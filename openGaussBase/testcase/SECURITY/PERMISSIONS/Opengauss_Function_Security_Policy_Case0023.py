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
Case Type   : Separation_policy
Case Name   : 给过期的用户重新设定有效期限
Description :
    1.用系统管理员用户或初始用户登录数据库
    2.修改过期用户时间：ALTER USER wf WITH VALID BEGIN '2016-11-10 08:00:00' VALID UNTIL '2056-11-10 08:00:00';
    3.登录用户
Expect      :
    1.数据库登录成功
    2.修改成功
    3.用户登录成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Privategrant(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('------------Opengauss_Function_Security_Policy_Case0023 start--------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.sh_primy = CommonSH('PrimaryDbUser')

    def test_schema(self):
        sql_cmd1 = f'''CREATE USER wf WITH PASSWORD '{macro.COMMON_PASSWD}' VALID BEGIN '2000-08-10 08:00:00' VALID UNTIL '2000-08-11 10:43:00';'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        sql_cmd2 = '''ALTER USER wf WITH VALID BEGIN '2016-11-10 08:00:00' VALID UNTIL '2056-11-10 08:00:00';'''
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.assertTrue(msg2.find("ALTER ROLE") > -1)
        excute_cmd3 = f'''
                    source {self.DB_ENV_PATH}
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U wf -W '{macro.COMMON_PASSWD}' -c 'select user;'
                '''
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find("wf") > -1)

    def tearDown(self):
        sql_cmd1 = '''drop user if exists wf cascade;'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.logger.info('--------------Opengauss_Function_Security_Policy_Case0023 finish--------------')
