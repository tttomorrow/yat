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
Case Name   : 在openGauss各主机上执行的linux shell命令名:arch,uname 命令
Description :
    1.显示机器的处理器架构
    2.显示正在使用的内核版本
Expect      :
    1.显示正确
    2.显示正确
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Log = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0015开始执行-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        Log.info('------------------显示机器的处理器架构------------------')
        arch_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "arch"'
        Log.info(arch_cmd)
        arch_msg = self.dbuser_node.sh(arch_cmd).result()
        Log.info(arch_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, arch_msg)

    def test_server_tools2(self):
        Log.info('------------------显示正在使用的内核版本------------------')
        uname_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "uname -r"'
        Log.info(uname_cmd)
        unam_msg = self.dbuser_node.sh(uname_cmd).result()
        Log.info(unam_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, unam_msg)

    def tearDown(self):
        Log.info('----------------无需清理环境-----------------------')
        Log.info('-----Opengauss_Function_Tools_gs_ssh_Case0015执行结束----')
