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
Case Name   : root用户检查SSD性能（不使用-U）
Description :
    root用户检查SSD性能（不使用-U）
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
        logger.info('--------------Opengauss_Function_Tools_gs_checkperf_Case0012start-------------------')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------root用户检查SSD性能（不使用-U）------------------')
        checkperf_cmd = f'''
                                    source {macro.DB_ENV_PATH}
                                    gs_checkperf  -i  SSD
                                    '''
        logger.info(checkperf_cmd)
        msg = self.rootNode.sh(checkperf_cmd).result()
        logger.info(msg)
        self.assertIn("Parameter '-U' is required for a user with the root permission",msg)

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_checkperf_Case0012finish------------------')
