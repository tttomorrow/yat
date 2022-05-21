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
Case Name   : 只审计用户登录成功，audit_login_logout=1
Description :
    步骤 1.设置gs_guc reload -N all -I all -c  "audit_login_logout=1"
    步骤 2.user003正确的用户、密码，登录数据库,退出；
    步骤 3.user003错误的用户、密码，登录数据库
    步骤 4.查看审计日志select * from pg_query_audit('{start_time}','{end_time}')
    where type like 'login%' or type like '%logout%' and username = 'user003';
    时间设在最接近登录数据库的时间
Expect      :
    步骤 1.设置成功
    步骤 2.登录成功，退出成功
    步骤 3.登录失败
    步骤 4.只查询到登录成功的记录
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
            '-----Opengauss_Function_Security_Auditing_Case0005 start----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        execute_cmd0 = f'source {self.DB_ENV_PATH};' \
                       f'gs_guc reload -N all -I all -c "audit_login_logout=1"'
        msg0 = self.userNode.sh(execute_cmd0).result()
        self.logger.info(msg0)
        sql_cmd1 = f'create user user003 with password \'' \
                   f'{macro.COMMON_PASSWD}\';'
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        time.sleep(5)
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        new_password2 = macro.COMMON_PASSWD.lower() + "qas"
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U user003 -W ' \
                      f'{macro.COMMON_PASSWD} -c "\\q";' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U user003 ' \
                      f'-W {new_password2} -c "\\q"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        time.sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd3 = f'select * from pg_query_audit(\'{start_time}\',\
                   \'{end_time}\');'
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd3}"'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertFalse(
            msg3.find('failed,authentication for user(user003)failed') > -1)
        self.assertTrue(msg3.find('success,the current user is:user003') > -1)
        self.assertFalse(msg3.find('user_logout') > -1)

    def tearDown(self):
        sql_cmd1 = 'drop user user003;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "audit_login_logout=7"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.logger.info(
            '-------Opengauss_Function_Security_Auditing_Case0005 end------')
