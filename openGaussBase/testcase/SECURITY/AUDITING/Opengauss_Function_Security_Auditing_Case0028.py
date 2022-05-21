"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
"""
Case Type   : security-auditing
Case Name   : 表示开启审计用户权限授予和回收功能,设置audit_grant_revoke=1
Description :
    1.登录数据库执行show audit_grant_revoke;
    2.给用户赋予权限，grant all privileges to user003;
    3.收回用户权限，revoke all privileges from user003;
    4登录数据库，查看审计日志SELECT * FROM pg_query_audit('$start_time','$end_time');时间设在最接近登录数据库的时间
Expect      :
    1.返回默认值1
    2.赋权成功
    3.权限回收成功
    4.查询到赋权、权限回收的信息
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Logger import Logger


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '-----Opengauss_Function_Security_Auditing_Case0028 start-----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        sql_cmd1 = f'create user user003 with password ' \
                   f'\'{macro.COMMON_PASSWD}\';' \
                   f'create table table001(id int);'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertTrue('CREATE ROLE' in msg1 and 'CREATE TABLE' in msg1)
        excute_cmd = f'source {self.DB_ENV_PATH};' \
                     f'gs_guc reload -N all -I all -c "audit_grant_revoke=0"'
        msg2 = self.userNode.sh(excute_cmd).result()
        self.logger.info(msg2)
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        time.sleep(5)
        sql_cmd3 = 'grant insert on table001 to user003;' \
                   'revoke insert on table001 from user003;'
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd3}"'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        time.sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd4 = f'select * from pg_query_audit(\'{start_time}\',\
                   \'{end_time}\');'''
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd4}"'
        msg4 = self.userNode.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.assertFalse(msg3.find('grant insert on table001 to user003') > -1)
        self.assertFalse(
            msg3.find('revoke insert on table001 from user003') > -1)

    def tearDown(self):
        sql_cmd1 = 'drop user user003;' \
                   'drop table table001;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "audit_grant_revoke=1"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        sql_cmd3 = 'show audit_grant_revoke;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'audit_grant_revoke', '1', '(1 row)',
                                  flag="1")
        self.logger.info(
            '-----Opengauss_Function_Security_Auditing_Case0028 end----')
