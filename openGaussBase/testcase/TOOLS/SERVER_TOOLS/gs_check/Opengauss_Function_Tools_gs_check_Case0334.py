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
Case Name   : 检查磁盘占用时指定告警阈值（不在1-99之间的整数范围内）
Description :
     1.指定告警阈值：gs_check -i CheckDataDiskUsage --disk-threshold="0"
     2.指定告警阈值：gs_check -i CheckDataDiskUsage --disk-threshold="50.5"
     3.指定告警阈值：gs_check -i CheckDataDiskUsage --disk-threshold="100"
Expect      :
     1.检查完成
     2.检查完成
     3.检查完成
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
        logger.info('--------------Opengauss_Function_Tools_gs_check_Case0334start-------------------')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------指定告警阈值为0------------------')
        check_cmd1 = f'''
                                source {macro.DB_ENV_PATH}
                                gs_check -i CheckDataDiskUsage --disk-threshold="0%"
                                '''
        logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        logger.info(msg1)
        self.assertIn('invalid literal for int() with base 10', msg1)
        logger.info('------------------指定告警阈值为50.5------------------')
        check_cmd2 = f'''
                                source {macro.DB_ENV_PATH}
                                gs_check -i CheckDataDiskUsage --disk-threshold="50.5%" 
                                 '''
        logger.info(check_cmd2)
        msg2 = self.dbuserNode.sh(check_cmd2).result()
        logger.info(msg2)
        self.assertIn('invalid literal for int() with base 10',msg2)
        logger.info('------------------指定告警阈值为100------------------')
        check_cmd3 = f'''
                                  source {macro.DB_ENV_PATH}
                                  gs_check -i CheckDataDiskUsage --disk-threshold="100%"
                                         '''
        logger.info(check_cmd3)
        msg3 = self.dbuserNode.sh(check_cmd3).result()
        logger.info(msg3)
        self.assertIn('invalid literal for int() with base 10', msg3)

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_check_Case0334finish------------------')