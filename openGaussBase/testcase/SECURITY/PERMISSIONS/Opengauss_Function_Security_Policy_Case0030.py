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
Case Type   : policy
Case Name   : 密码为A-Z大写字母的最少要求个数password_min_uppercase=1
Description :
    1.在postgres.conf中设置password_min_uppercase=1，重启数据库生效
    2.初始用户执行：create user $user! with password '$passwd1';(密码含一个大写字母)
    create user $user2 with password '$passwd2';(密码无大写字母)
Expect      :
    1.设置成功，数据库重启成功
    2.CREATE ROLE
    提示密码至少包含一个大写字母
History     :
"""
import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info('pengauss_Function_Security_Policy_Case0030 start')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.new_password1 = macro.COMMON_PASSWD.capitalize()
        self.new_password2 = macro.COMMON_PASSWD.lower()
        self.Constant = Constant()
        self.user = 'u_security_policy_0030'
        self.userNode = Node(node='PrimaryDbUser')

    def test_policy(self):
        logger.info('----修改password_min_uppercase参数为1----')
        exe_cmd0 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"password_min_uppercase=1"'
        msg0 = self.userNode.sh(exe_cmd0).result()
        logger.info(msg0)
        logger.info('------------create user ---------------')
        sql_cmd1 = f'drop user if exist {self.user};' \
            f'create user {self.user} password \'{self.new_password1}\';' \
            f'drop user {self.user};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        sql_cmd2 = f'create user {self.user} with password ' \
                   f'\'{self.new_password2}\';'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn(self.Constant.PASSWORD_CONTAIN_AT_LEAST_MSG, msg2)

    def tearDown(self):
        logger.info('-----------恢复配置，并清理环境-----------')
        exe_cmd0 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"password_min_uppercase=3"'
        msg0 = self.userNode.sh(exe_cmd0).result()
        logger.info(msg0)
        sql_cmd1 = f'drop user {self.user} cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info('Opengauss_Function_Security_Policy_Case0030 finish')
