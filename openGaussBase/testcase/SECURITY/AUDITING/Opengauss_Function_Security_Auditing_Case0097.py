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
Case Name   : 拥有AUDITADMIN属性的用户查看审计记录
Description :
    1.创建auditadmin属性的用户，CREATE USER audit_admin WITH AUDITADMIN
     password "$PASSWORD";
    2.用audit_admin 用户登录数据库，创、删表：create table table01(id, int)
    ;drop table table01;查看审计记录， select count(*) from
    pg_query_audit('{start_time}','{end_time}') where username = 'audit_admin';
    3.删除用户
Expect      :
    1.创建成功
    2.查询到审计记录数目为4
    3.删除成功
History     :
"""
import unittest
import datetime
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Logger import Logger


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '-----Opengauss_Function_Security_Auditing_Case0097 start-----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        time.sleep(5)
        sql_cmd1 = f'CREATE USER audit_admin WITH AUDITADMIN password ' \
                   f'\'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'sql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U audit_admin -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "\q"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        time.sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd3 = f'select * from pg_query_audit(\'{start_time}\',\
                   \'{end_time}\');'
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U audit_admin -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd3}"'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(
            msg3.find('CREATE USER audit_admin WITH AUDITADMIN password') > -1)

    def tearDown(self):
        sql_cmd1 = 'drop user audit_admin;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.logger.info(
            '-----Opengauss_Function_Security_Auditing_Case0097 end-----')
