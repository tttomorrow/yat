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
Case Name   : 密码为A-Z大写字母的最少要求个数password_min_uppercase=0
Description :
    1.用系统管理员用户或初始用户登录数据库
    2.创建一个用户user1，起始时间等于结束时间：CREATE USER wf WITH PASSWORD
    '{macro.COMMON_PASSWD}' VALID BEGIN
Expect      :
    1.数据库登录成功
    2.返回报：The expiration time could not be earlier than the starting time
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info(
            '------Opengauss_Function_Security_Policy_Case0029 start-------')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_policy(self):
        logger.info('------------create user --------------')
        sql_cmd0 = f'show password_min_uppercase;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'password_min_uppercase', '0',
                                  '(1 row)', flag='1')
        sql_cmd1 = f'create user wf with password \'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        sql_cmd2 = 'select user;'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U  wf -W ' \
                      f'{macro.COMMON_PASSWD} -c "{sql_cmd2}"'
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'current_user', 'wf', '(1 row)',
                                  flag="1")

    def tearDown(self):
        logger.info('-----------清理环境-----------')
        sql_cmd1 = 'drop user if exists wf cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info(
            '------Opengauss_Function_Security_Policy_Case0029 finish-----')
