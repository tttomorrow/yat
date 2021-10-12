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
Case Name   : 在openGauss各主机上执行的linux shell命令名:netstat命令
Description :
    netstat命令可以显示当前网络的运行状态
    1.列出所有端口
    2.仅列出有在 Listen (**)状态的端口
    3.在netstat 输出中显示 PID 和进程名称
Expect      :
    1.显示所有端口
    2.显示所有在listen状态的端口
    3.显示PID 和进程名称
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
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0019开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        Log.info('------------------列出所有端口------------------')
        netstat_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "netstat -a"'
        Log.info(netstat_cmd)
        netstat_msg = self.dbuser_node.sh(netstat_cmd).result()
        Log.info(netstat_msg)
        self.assertIn('Active Internet connections '
            '(servers and established)', netstat_msg)

        Log.info('-----仅列出有在 Listen (**)状态的端口-----')
        netstat_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "netstat -l"'
        Log.info(netstat_cmd)
        netstat_msg = self.dbuser_node.sh(netstat_cmd).result()
        Log.info(netstat_msg)
        self.assertIn('Active UNIX domain sockets (only servers)', netstat_msg)
        self.assertIn('LISTENING', netstat_msg)

    def tearDown(self):
        Log.info('----------------无需清理环境-----------------------')
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0019执行结束----')
