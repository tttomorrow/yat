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
Case Type   : 服务端工具
Case Name   : 在openGauss各主机上执行的linux shell命令名:ps,top命令
Description :
    1.ps命令：查看当前运行的进程状态
    1.1显示当前所有进程环境变量及进程间关系
    1.2显示当前所有进程
    1.3与grep联用查找某进程
    2.top命令：显示当前系统正在执行的进程的相关信息，
    包括进程ID、内存占用率、CPU占用率等
Expect      :
    1.1显示正确
    1.2显示正确
    1.3查找成功
    2.1显示正确
    2.2显示正确
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
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0014开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        Log.info('----显示当前所有进程环境变量及进程间关系----')
        ps_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ps -ef"'
        Log.info(ps_cmd)
        ps_cmd = self.dbuser_node.sh(ps_cmd).result()
        Log.info(ps_cmd)
        self.assertIn(self.constant.gs_ssh_success_msg, ps_cmd)

        Log.info('----显示当前所有进程----')
        ps_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ps a" '
        Log.info(ps_cmd)
        ps_cmd = self.dbuser_node.sh(ps_cmd).result()
        Log.info(ps_cmd)
        self.assertIn(self.constant.gs_ssh_success_msg, ps_cmd)

        Log.info('------------------与grep联用查找某进程------------------')
        ps_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c " ps -aux | grep apache"'
        Log.info(ps_cmd)
        ps_cmd = self.dbuser_node.sh(ps_cmd).result()
        Log.info(ps_cmd)
        self.assertIn(self.constant.gs_ssh_success_msg, ps_cmd)

    def tearDown(self):
        Log.info('----------------无需清理环境-----------------------')
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0014执行结束----')
