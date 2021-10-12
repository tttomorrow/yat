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
Case Type   : security
Case Name   : 修改密码有效时间为1000，-1
Description :
    1.登录数据库，执行gs_guc set -N all -I all -c "password_effect_time=1000"
    2.gs_guc set -N all -I all -c "password_effect_time=-1"
Expect      :
    1.设置失败，参数超范围
    2.设置失败，参数超范围
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
            '---Opengauss_Function_Security_Authentication_Case0006 start---')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_policy(self):
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -N all -I all ' \
                      f'-c "password_effect_time=1000"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertTrue(msg1.find(
            'ERROR: The value 1000 is outside the valid range for parameter '
            '"password_effect_time" (0 .. 999)') > -1)
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -N all -I all -c "password_effect_time=-1"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertTrue(msg1.find('ERROR: The value -1 is outside the valid '
                                  'range for parameter '
                                  '"password_effect_time" (0 .. 999)') > -1)

    def tearDown(self):
        logger.info(
            '---Opengauss_Function_Security_Authentication_Case0006 finish---')
