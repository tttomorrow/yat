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
Case Name   : 用户检查CPU使用率，不指定检查结果输出文件夹路径
Description :
    用户检查CPU使用率，不指定检查结果输出文件夹路径： gs_check -i CheckCPU -o
Expect      :
    检查失败
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
        logger.info('--------------Opengauss_Function_Tools_gs_check_Case0308start-------------------')
        self.dbuserNode = Node('dbuser')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------运行openGauss的用户检查CPU使用率,不指定检查结果输出文件夹路径------------------')
        check_cmd1 = f'''
                                source {macro.DB_ENV_PATH}
                                gs_check -i CheckCPU  -o 
                                '''
        logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        logger.info(msg1)
        self.assertIn('-o requires argument',msg1)

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_check_Case0308finish------------------')
