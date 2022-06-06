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
Case Type   : security-policy
Case Name   : 密码和用户名倒写不能相同
Description :
    1初始用户执行：create user wfang_01_tt with password 'tt_10_gnafw';
Expect      :
    1.Password should not equal to the reverse of rolname
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('Opengauss_Function_Security_Policy_Case0056 start')
        self.userNode = Node('PrimaryDbUser')
        self.user = "wfang_01_tt"
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.sh_primy = CommonSH('PrimaryDbUser')

    def test_policy(self):
        self.logger.info('-----create user || table---------')
        password = ''.join(reversed(self.user))
        sql_cmd1 = f'''create user {self.user} with password '{password}';'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertIn(self.Constant.PASSWORD_SHOULD_NOT_EQUAL_MSG, msg1)

    def tearDown(self):
        sql_cmd1 = f'''drop user {self.user};'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.logger.info('Opengauss_Function_Security_Policy_Case0056 finish')
