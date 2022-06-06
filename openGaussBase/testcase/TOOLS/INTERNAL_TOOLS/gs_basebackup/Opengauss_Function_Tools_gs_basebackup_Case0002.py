"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

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
Case Type   : 工具-GS_BASEBACKUP
Case Name   : 查看版本号显示是否正确
Description :
    1、执行：gs_basebackup -V
Expect      :
    1、正确显示版本号，与gaussdb -V显示一致
History     :
"""

import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.Logger import Logger


class GsBaseBackUpVesion(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.LOG = Logger()
        self.Command_cmd = f"source {macro.DB_ENV_PATH}; gs_basebackup -V"
        self.Expect_Command_cmd = f"source {macro.DB_ENV_PATH}; gaussdb -V"
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0002 start----')

    def test_server_tools(self):
        self.LOG.info('----执行：gs_basebackup -V----')
        self.LOG.info(self.Command_cmd)
        gs_basebachkup_result = \
            self.Primary_User_Node.sh(self.Command_cmd).result()
        self.LOG.info(gs_basebachkup_result)

        self.LOG.info('----执行：gaussdb -V----')
        self.LOG.info(self.Command_cmd)
        gaussdb_result = self.Primary_User_Node.sh(self.Command_cmd).result()
        self.LOG.info(gaussdb_result)

        self.assertEqual(gs_basebachkup_result, gaussdb_result)

    def tearDown(self):
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0002 end----')
