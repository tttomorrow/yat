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
Case Name   : gs_om工具SSL证书替换时不指定路径
Description :
    gs_om工具SSL证书替换时不指定路径
Expect      :
    gs_om工具SSL证书替换时不指定路径
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0013start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        self.logger.info('-----gs_om工具SSL证书替换时不指定路径------')
        check_cmd1 = f'''
                                        source {macro.DB_ENV_PATH};
                                        gs_om -t cert; '''
        self.logger.info(check_cmd1)
        msg = self.dbuser_node.sh(check_cmd1).result()
        self.logger.info(msg)
        self.assertIn("Parameter '--cert-file or --rollback' is required",
                      msg)

    def tearDown(self):
        self.logger.info('--------------无需清理环境-------------------')
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0013finish--')
