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
Case Type   : 服务端工具
Case Name   : 使用--skip-root-items跳过需要root权限执行的检查项（CheckSshdConfig）
Description :
     1.跳过sshd服务配置是否正确检查，检查CPU：gs_check -i CheckSshdConfig,CheckCPU   --skip-root-items
     2.先检查CPU再跳过sshd服务配置是否正确检查：gs_check -i CheckCPU,CheckSshdConfig   --skip-root-items
     3.直接跳过sshd服务配置是否正确检查（单项检查）：gs_check -i CheckSshdConfig   --skip-root-items
Expect      :
    1.检查完成
    2.检查完成
    3.检查失败
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
        logger.info('--------------Opengauss_Function_Tools_gs_check_Case0317start-------------------')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------跳过sshd服务配置是否正确检查，检查CPU------------------')
        check_cmd1 = f'''
                                source {macro.DB_ENV_PATH}
                                gs_check -i CheckSshdConfig,CheckCPU   --skip-root-items 
                                '''
        logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        logger.info(msg1)
        flag = (self.Constant.GS_CHECK_SUCCESS_MSG2[0] in msg1 or self.Constant.GS_CHECK_SUCCESS_MSG2[1] in msg1) and \
               self.Constant.GS_CHECK_SUCCESS_MSG2[2] in msg1
        self.assertTrue(flag)
        logger.info('------------------先检查CPU再跳过sshd服务配置是否正确检查------------------')
        check_cmd2 = f'''
                                source {macro.DB_ENV_PATH}
                                gs_check -i CheckCPU,CheckSshdConfig   --skip-root-items 
                                 '''
        logger.info(check_cmd2)
        msg2 = self.dbuserNode.sh(check_cmd2).result()
        logger.info(msg2)
        flag = (self.Constant.GS_CHECK_SUCCESS_MSG2[0] in msg2 or self.Constant.GS_CHECK_SUCCESS_MSG2[1] in msg2) and \
               self.Constant.GS_CHECK_SUCCESS_MSG2[2] in msg2
        self.assertTrue(flag)
        logger.info('------------------直接跳过sshd服务配置是否正确检查（单项检查）------------------')
        check_cmd3 = f'''
                                        source {macro.DB_ENV_PATH}
                                        gs_check -i CheckSshdConfig   --skip-root-items 
                                         '''
        logger.info(check_cmd3)
        msg3 = self.dbuserNode.sh(check_cmd3).result()
        logger.info(msg3)
        self.assertIn('ERROR: No check item can be performed, please confirm the input parameters',msg3)

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_check_Case0317finish------------------')
