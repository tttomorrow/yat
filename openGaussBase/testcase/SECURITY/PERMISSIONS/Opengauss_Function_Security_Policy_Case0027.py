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
Case Name   : 显示默认密码策略
Description :
    1.用系统管理员用户或初始用户登录数据库
    2.创建一个用户user1，起始时间等于结束时间：CREATE USER wf WITH PASSWORD
    '{macro.COMMON_PASSWD}' VALID BEGIN
Expect      :
    1.数据库登录成功
    2.返回报错：The expiration time could not be earlier than the starting time
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Privategrant(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '-------Opengauss_Function_Security_Policy_Case0027 start------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()

    def test_user(self):
        self.logger.info('----------create user || table---------')
        sql_cmd1 = 'SHOW password_policy;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p' \
                      f' {self.userNode.db_port} -c "{sql_cmd1}"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.common.equal_sql_mdg(msg1, 'password_policy', '1', '(1 row)',
                                  flag='1')

    def tearDown(self):
            self.logger.info(
                '------Opengauss_Function_Security_Policy_Case0027 finish----')
