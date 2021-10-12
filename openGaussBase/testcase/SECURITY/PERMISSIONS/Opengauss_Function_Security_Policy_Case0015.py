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
Case Name： 设置password_lock_time=366，返回报错
Create at:  2020/11/10
Description:  1.设置参数：gs_guc set -N all -I all -c "password_lock_time=366"
Expect:  1.参数报错提示：超出范围
History:
'''
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger

class Privategrant(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('------------Opengauss_Function_Security_Policy_Case0015 start--------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
    def test_schema(self):
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gs_guc set -N all -I all -c "password_lock_time=366";
                    '''
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find("The value 366 is outside the valid range for parameter") > -1)

    def tearDown(self):
        self.logger.info('--------------Opengauss_Function_Security_Policy_Case0015 end---------------')
