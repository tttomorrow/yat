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
Case Name   : 检查open gaussXML配置文件（文件路径或名称不正确）
Description : 检查open gaussXML配置文件（文件路径或名称不正确）
Expect      : 检查失败
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('---Opengauss_Function_Tools_gs_checkos_Case0048start---')
        self.rootNode = Node('default')

    def test_server_tools(self):
        LOG.info('----检查open gaussXML配置文件（文件路径或名称不正确）----')
        checkos_cmd = f'''source {macro.DB_ENV_PATH}
            gs_checkos  -i A -X /home/checkos/checkos.xml
            '''
        LOG.info(checkos_cmd)
        msg = self.rootNode.sh(checkos_cmd).result()
        LOG.info(msg)
        self.assertIn('The /home/checkos/checkos.xml does not exist', msg)

    def tearDown(self):
        LOG.info('--------------无需清理环境-------------------')
        LOG.info('--Opengauss_Function_Tools_gs_checkos_Case0048finish--')