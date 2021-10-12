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
Case Type   : policy
Case Name   : 密码少于最小长度要求password_min_length=1000
Description :
    1.执行：gs_guc set -N all -I all -c 'password_min_special=1000'
Expect      :
    1.报错，参数值无效
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
common = Common()
sh_primy = CommonSH('PrimaryDbUser')


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info('---Opengauss_Function_Security_Policy_Case0048 start---')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()

    def test_policy(self):
        logger.info('----------create user--------------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -N all -I all -c "password_min_length=1000"'
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.OUTSIDE_VALID_RANGE_MSG, msg1)

    def tearDown(self):
            logger.info(
                '----Opengauss_Function_Security_Policy_Case0048 finish-----')
