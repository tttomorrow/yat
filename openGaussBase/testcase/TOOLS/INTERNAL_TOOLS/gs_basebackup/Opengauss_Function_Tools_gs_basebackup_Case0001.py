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
Case Type   : 工具-GS_BASEBACKUP
Case Name   : 查看帮助文档是否正确
Description :
    1、执行：gs_basebackup -?
Expect      :
    1、帮助文档正确显示
History     :
"""

import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.Logger import Logger


class GsBaseBackUpHelp(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.LOG = Logger()
        self.Command_cmd = f"source {macro.DB_ENV_PATH}; gs_basebackup -?"
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0001 start----')
        self.Return_Info = {
            'tips': 'gs_basebackup takes a base backup of ' +
                    'a running openGauss server.',
            'detail': {'Usage': 'gs_basebackup [OPTION]...',
                       'Options controlling the output': (
                           '-D, --pgdata',
                           '-F, --format',
                           '-T, --tablespace-mapping',
                           '-x, --xlog',
                           '-X, --xlog-method',
                           '-z, --gzip',
                           '-Z, --compress'),
                       'General options': (
                           '-c, --checkpoint',
                           '-l, --label',
                           '-P, --progress',
                           '-v, --verbose',
                           '-V, --version',
                           '-?, --help'),
                       'Connection options': (
                           '-h, --host',
                           '-p, --port',
                           '-s, --status-interval',
                           '-U, --username',
                           '-w, --no-password',
                           '-W, --password')}}

    def test_server_tools(self):
        self.LOG.info('----执行：gs_basebackup -?----')
        self.LOG.info(self.Command_cmd)
        result = self.Primary_User_Node.sh(self.Command_cmd).result()
        self.LOG.info(result)
        for out_value in self.Return_Info.values():
            if type(out_value) is not dict:
                self.assertIn(out_value, result)
            else:
                for inner_key in out_value:
                    self.assertIn(inner_key, result)
                for inner_value in out_value:
                    if type(inner_value) is not tuple:
                        self.assertIn(inner_value, result)
                    else:
                        for arg in inner_value:
                            self.assertIn(arg, inner_value)

    def tearDown(self):
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0001 end----')
