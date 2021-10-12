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
Case Type   : security-policy
Case Name   : 设置加密算法的配置参数password_encryption_type设置为0
Description :
    1.设置参数password_encryption_type=0：gs_guc reload -N all -I all -c
    "password_encryption_type=0"
    2.登录数据库
Expect      :
    1.参数设定成功
    2.登录数据库成功，show password_encryption_type；返回0
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
            '------Opengauss_Function_Security_Policy_Case0025 start-----')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_policy(self):
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all ' \
                      f'-c "password_encryption_type=0"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        sql_cmd2 = 'show password_encryption_type;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'password_encryption_type', '0',
                                  '(1 row)', flag="1")

    def tearDown(self):
        logger.info('-----------恢复配置-----------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all' \
                      f' -c "password_encryption_type=2"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        sql_cmd2 = 'show password_encryption_type;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'password_encryption_type', '2',
                                  '(1 row)', flag="1")
        logger.info(
            '------Opengauss_Function_Security_Policy_Case0025 finish-----')
