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
Case Name   : 检查系统参数同时设置参数系统的参数的期望值
Description :
    检查系统参数同时设置参数系统的参数的期望值
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
        logger.info('--------------Opengauss_Function_Tools_gs_checkos_Case0032start-------------------')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------检查系统参数同时设置参数系统的参数的期望值------------------')
        checkos_cmd = f'''
                                    source {macro.DB_ENV_PATH}
                                    gs_checkos -i   A6,B1
                                    '''
        logger.info(checkos_cmd)
        msg = self.rootNode.sh(checkos_cmd).result()
        logger.info(msg)
        self.assertIn("Checking items and setting items can't be used together",msg)

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_checkos_Case0032finish------------------')
