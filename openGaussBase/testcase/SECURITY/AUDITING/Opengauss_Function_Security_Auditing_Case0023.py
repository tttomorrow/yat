"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Name   : 开启用户登录、退出的审计功能，audit_user_violation默认值1
Description :
    1.登陆数据库，执行show audit_user_violation;
    2.数据库默认用户创建一个表table01,create table table01(id int);
    3.普通用户登录访问table01,select * from table01;
    4登录数据库，查看审计日志select * from pg_query_audit('{start_time}',
    '{end_time}') where username = 'user003';时间设在最接近登录数据库的时间
Expect      :
    1.显示默认值1
    2.停止成功
    3.启动成功
    4.查询到启动/停止的信息
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
            '----Opengauss_Function_Security_Auditing_Case0023 start----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        sql_cmd1 = f'create table table01(id int);create user user003 with ' \
                   f'password \'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.assertTrue('CREATE TABLE' in msg1 and 'CREATE ROLE' in msg1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"audit_user_violation=1"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        time.sleep(5)
        sql_cmd2 = 'select * from table01;'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U user003 -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        time.sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd3 = f'select * from pg_query_audit(\'{start_time}\',\
                   \'{end_time}\') where type = \'user_violation\' and ' \
                   f'username = \'user003\';'
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd3}"'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(
            msg3.find('permission denied for relation table01') > -1)

    def tearDown(self):
        sql_cmd1 = 'drop table table01;' \
                   'drop user user003;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"audit_user_violation=0"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        sql_cmd3 = 'show audit_user_violation;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'audit_user_violation', '0', '(1 row)',
                                  flag="1")
        self.logger.info(
            '----Opengauss_Function_Security_Auditing_Case0023 end----')
