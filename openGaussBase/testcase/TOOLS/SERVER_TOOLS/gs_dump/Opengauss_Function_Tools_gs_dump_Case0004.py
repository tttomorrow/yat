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
Case Name   : gs_dump工具显示版本号信息（异常）
Description :
    显示版本号信息：gs_dump --V
Expect      :
    显示失败，合理报错
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-----Opengauss_Function_Tools_gs_dump_Case0004start-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('------------------版本号信息------------------')
        check_cmd1 = f'''source {macro.DB_ENV_PATH}
                        gs_dump --V'''
        LOG.info(check_cmd1)
        msg1 = self.dbuser_node.sh(check_cmd1).result()
        LOG.info(msg1)
        self.assertIn('Try "gs_dump --help" for more information', msg1)

    def tearDown(self):
        LOG.info('--------------无需清理环境-------------------')
        LOG.info('-----Opengauss_Function_Tools_gs_dump_Case0004finish-----')
