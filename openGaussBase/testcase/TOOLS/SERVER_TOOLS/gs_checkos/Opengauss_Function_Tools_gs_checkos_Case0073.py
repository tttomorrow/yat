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
Case Name   : omm用户检查操作系统信息
Description :
    omm用户检查操作系统信息
Expect      :
    执行失败
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
        logger.info('--------------Opengauss_Function_Tools_gs_checkos_Case0073start-------------------')
        self.dbuserNode = Node('dbuser')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------omm用户检查操作系统信息------------------')
        checkos_cmd = f'''
                                    source {macro.DB_ENV_PATH}
                                    gs_checkos  -i A
                                    '''
        logger.info(checkos_cmd)
        msg = self.dbuserNode.sh(checkos_cmd).result()
        logger.info(msg)
        self.assertIn('gs_checkos: command not found',msg)

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_checkos_Case0073finish------------------')
