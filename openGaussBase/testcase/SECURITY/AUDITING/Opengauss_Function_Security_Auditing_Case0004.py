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
Case Name   : 关闭用户登录、退出的审计功能，audit_login_logout=0
Description :
    步骤 1.设置gs_guc reload -N all -I all -c "audit_login_logout=0"
    步骤 2.登录数据库；
    步骤 3.select * from pg_query_audit('{start_time}','{end_time}') where type
     like 'login%' or type like '%logout%' and username = 'user03';时间设在最接
     近登录数据库的时间
Expect      :
    步骤 1.设置成功
    步骤 2.登录成功
    步骤 3.未查询到用户登录、退出的记录
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
            '----Opengauss_Function_Security_Auditing_Case0004 start---')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        execute_cmd0 = f'source {self.DB_ENV_PATH};gs_guc reload -N all -I ' \
                       f'all -c "audit_login_logout=0"'
        msg0 = self.userNode.sh(execute_cmd0).result()
        self.logger.info(msg0)
        sql_cmd1 = f'create user user03 with password \'' \
                   f'{macro.COMMON_PASSWD}\';'

        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        time.sleep(5)
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        new_password2 = macro.COMMON_PASSWD.lower() + "qas"
        excute_cmd2 = f'source {self.DB_ENV_PATH};gsql -d ' \
                      f'{self.userNode.db_name} -p {self.userNode.db_port} ' \
                      f'-U user03 -W {macro.COMMON_PASSWD} -c "\\q";' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U user03 -W ' \
                      f'{new_password2} -c "\\q"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)

        time.sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd3 = f'select * from pg_query_audit(\'{start_time}\',\
                   \'{end_time}\') where username = \'user03\';'
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd3}"'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertFalse(
            msg3.find('failed,authentication for user(user03)failed') > -1)
        self.assertFalse(msg3.find('success,the current user is:user03') > -1)
        self.assertFalse(msg3.find('user_logout') > -1)

    def tearDown(self):
        sql_cmd1 = 'drop user user03;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};gs_guc reload -N all -I ' \
                      f'all -c "audit_login_logout=7"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.logger.info(
            '------Opengauss_Function_Security_Auditing_Case0004 end------')
