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
Case Name   : omm用户检查XML差异 （合理报错，暂不支持）
Description :
    1.由root用户切换到omm用户下
    2.在非本地模式下检查： gs_check -i CheckConfigFileDiff
    3.在本地模式下检查： gs_check -i CheckConfigFileDiff -L
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
        logger.info('--------------Opengauss_Function_Tools_gs_check_Case0147start-------------------')
        self.dbuserNode = Node('dbuser')
        self.Constant = Constant()


    def test_server_tools(self):
        logger.info('------------------omm用户在非本地模式下检查XML差异------------------')
        check_cmd1 = f'''
                            source {macro.DB_ENV_PATH}
                            gs_check -i CheckConfigFileDiff
                            '''

        logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        logger.info(msg1)
        self.assertIn(
            'ERROR: There were errors when parsing these items: CheckConfigFileDiff. maybe items name is incorrect',
            msg1)
        logger.info('------------------omm用户在本地模式下检查XML差异------------------')
        check_cmd2 = f'''
                            source {macro.DB_ENV_PATH}
                            gs_check -i CheckConfigFileDiff -L
                            '''
        logger.info(check_cmd2)
        msg2 = self.dbuserNode.sh(check_cmd2).result()
        logger.info(msg2)
        self.assertIn(
            'ERROR: There were errors when parsing these items: CheckConfigFileDiff. maybe items name is incorrect',
            msg2)


    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_check_Case0147finish------------------')
