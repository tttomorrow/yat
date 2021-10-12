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
Case Name   : omm用户检查磁盘故障
Description :
    1.由root用户切换到omm用户下
    2.在非本地模式下检查： gs_check -i CheckDiskFailure
    3.在本地模式下检查： gs_check -i CheckDiskFailure -L
Expect      :
    1.切换到omm用户下
    2.非本地模式下检查完成
    3.本地模式下执行检查完成
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
        logger.info('--------------Opengauss_Function_Tools_gs_check_Case0191start-------------------')
        self.dbuserNode = Node('dbuser')
        self.Constant = Constant()

    def test_server_tools(self):
        logger.info('------------------omm用户在非本地模式下检查磁盘故障------------------')
        check_cmd1 = f'''
                            source {macro.DB_ENV_PATH}
                            gs_check -i CheckDiskFailure
                            '''

        logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        logger.info(msg1)
        flag = (self.Constant.GS_CHECK_SUCCESS_MSG2[0] in msg1 or self.Constant.GS_CHECK_SUCCESS_MSG2[1] in msg1) and \
               self.Constant.GS_CHECK_SUCCESS_MSG2[2] in msg1
        self.assertTrue(flag)
        logger.info('------------------omm用户在本地模式下检查磁盘故障------------------')
        check_cmd2 = f'''
                            source {macro.DB_ENV_PATH}
                            gs_check -i CheckDiskFailure -L
                            '''
        logger.info(check_cmd2)
        msg2 = self.dbuserNode.sh(check_cmd2).result()
        logger.info(msg2)
        check_result_flag = False
        for single_msg in self.Constant.GS_CHECK_SUCCESS_MSG1:
            if single_msg in msg2:
                check_result_flag = True
        self.assertTrue(check_result_flag)

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_check_Case0191finish------------------')
