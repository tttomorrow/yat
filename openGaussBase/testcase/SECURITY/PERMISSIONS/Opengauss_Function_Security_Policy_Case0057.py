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
'''
Case Type   : policy
Case Name   : 密码和用户名相同
Create at   :  2020/9/23
Description :  密码和用户名相同
'''
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Privategrant(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-------------Opengauss_Function_Security_Policy_Case0057 start--------------')
        self.userNode = Node('PrimaryDbUser')
        self.user = "wfang_01_tt"
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_policy(self):
        self.logger.info('----------------------------create user || table-----------------------------')
        sql_cmd1 = f'''create user {self.user} with password '{self.user}';'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertIn(self.Constant.PASSWORD_SHOULD_NOT_EQUAL_MSG, msg1)

    def tearDown(self):
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        try:
            db_status = self.sh_primy.get_db_instance_status()
            self.logger.info(db_status)
            if db_status:
                pass
            else:
                is_started = self.sh_primy.start_db_cluster()
                self.assertTrue(is_started)
                self.logger.info(f'db_status: {is_started}')
        finally:
            sql_cmd1 = f'''drop user {self.user};'''
            msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
            self.logger.info(msg1)
        self.logger.info('----------------Opengauss_Function_Security_Policy_Case0057 finish----------------')
