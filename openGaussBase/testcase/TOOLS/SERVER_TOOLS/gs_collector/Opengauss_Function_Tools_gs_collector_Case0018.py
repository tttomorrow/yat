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
Case Name   : 收集日志信息并设置收集速率为负整数或小数
Description :
        1.收集日志信息并设置收集速率为负整数
        2.收集日志信息并设置收集速率为小数
Expect      :
        1.收集失败
        2.收集失败
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
        logger.info('--------------Opengauss_Function_Tools_gs_collector_Case0018start-------------------')
        self.dbuserNode = Node('dbuser')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------收集日志信息并设置收集速率为负整数------------------')
        check_cmd1 = f'''
                        source {macro.DB_ENV_PATH}
                        gs_collector --begin-time="20200909 10:10"  --end-time="20200914 11:05"  --speed-limit=-10
                                '''
        logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        logger.info(msg1)
        self.assertIn("The parameter '--speed-limit' type should be a nonnegative integer", msg1)
        logger.info('------------------收集日志信息并设置收集速率为小数------------------')
        check_cmd2 = f'''
                        source {macro.DB_ENV_PATH}
                        gs_collector --begin-time="20200909 10:10"  --end-time="20200914 11:05"  --speed-limit=5.8
                                        '''
        logger.info(check_cmd2)
        msg2 = self.dbuserNode.sh(check_cmd2).result()
        logger.info(msg2)
        self.assertIn("The parameter '--speed-limit' type should be a nonnegative integer", msg2)

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_collector_Case0018finish------------------')