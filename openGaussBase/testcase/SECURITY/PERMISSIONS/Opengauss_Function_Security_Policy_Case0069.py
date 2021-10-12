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
Case Type： security-policy
Case Name： 置密码不可重用次数设置为1.5
Create at:  2020/11/10
Description:  1.设置参数：gs_guc reload -N all -I all -c "password_reuse_max=1.5;
Expect:  1.报错，参数不支持浮点型数
History:
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
        self.logger.info('------------Opengauss_Function_Security_Policy_Case0069 start--------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
    def test_schema(self):
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gs_guc set -N all -I all -c 'password_reuse_max=1.5';
                    '''
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find("The parameter \"password_reuse_max\" requires an integer value") > -1)

    def tearDown(self):
        self.logger.info('--------------Opengauss_Function_Security_Policy_Case0069 end---------------')
