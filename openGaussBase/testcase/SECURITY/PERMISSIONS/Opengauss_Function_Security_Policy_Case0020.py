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
Case Type   : Separation_policy
Case Name   : 设定用户开始时间大于结束时间
Description :
    1.用系统管理员用户或初始用户登录数据库
    2.创建一个用户user1,起始时间大于结束时间：CREATE USER user1 WITH PASSWORD '{macro.COMMON_PASSWD}' VALID BEGIN
Expect      :
    1.数据库登录成功
    2. 返回报错信息：The expiration time could not be earlier than the starting time
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
        self.logger.info('------------Opengauss_Function_Security_Policy_Case0020 start--------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.sh_primy = CommonSH('PrimaryDbUser')

    def test_schema(self):
        sql_cmd1 = f'''CREATE USER user1 WITH PASSWORD '{macro.COMMON_PASSWD}' VALID BEGIN '2022-08-10 08:00:00' VALID UNTIL '2020-08-11 10:43:00';'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertTrue(msg1.find("The expiration time could not be earlier than the starting time") > -1)

    def tearDown(self):
        sql_cmd1 = f'''DROP USER user1;'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.logger.info('--------------Opengauss_Function_Security_Policy_Case0020 finish--------------')
