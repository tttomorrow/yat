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
Case Type   : 服务端工具
Case Name   : 使用--format参数设置检查结果报告的格式为text
Description :
     1.设置格式时，后面不添加参数：gs_check -i CheckCPU  --format
     2.设置格式为text：gs_check -i CheckCPU --format text
Expect      :
     1.检查失败
     2.检查失败
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()

class Tools(unittest.TestCase):
    def setUp(self):
        logger.info('--------------Opengauss_Function_Tools_gs_check_Case0336start-------------------')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------设置格式时，后面不添加参数------------------')
        check_cmd1 = f'''
                                source {macro.DB_ENV_PATH}
                                gs_check -i CheckCPU  --format
                                '''
        logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        logger.info(msg1)
        self.assertIn('option --format requires argument', msg1)
        logger.info('------------------设置格式为text------------------')
        check_cmd2 = f'''
                                source {macro.DB_ENV_PATH}
                                gs_check -i CheckCPU --format text 
                                 '''
        logger.info(check_cmd2)
        msg2 = self.dbuserNode.sh(check_cmd2).result()
        logger.info(msg2)
        self.assertIn('ERROR: Format text is not available,the valid format is default,json',msg2)

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_check_Case0336finish------------------')