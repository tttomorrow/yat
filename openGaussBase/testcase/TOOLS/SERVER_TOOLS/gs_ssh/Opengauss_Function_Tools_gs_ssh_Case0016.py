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
Case Name   : Opengauss_Function_Tools_gs_ssh_Case0016
Description :
    1. 显示内存使用情况
    2.以总和的形式显示内存的使用信息
    3.以kb为单位显示内存使用情况
Expect      :
    1.显示正确
    2.显示正确
    3.显示正确
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
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0016开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        Log.info('------------------显示内存使用情况------------------')
        free_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "free"'
        Log.info(free_cmd)
        free_msg = self.dbuser_node.sh(free_cmd).result()
        Log.info(free_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, free_msg)

        Log.info('------以总和的形式显示内存的使用信息------')
        free_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "free -t"'
        Log.info(free_cmd)
        free_msg = self.dbuser_node.sh(free_cmd).result()
        Log.info(free_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, free_msg)

        Log.info('-------------以kb为单位显示内存使用情况--------------')
        free_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "free -k"'
        Log.info(free_cmd)
        free_msg = self.dbuser_node.sh(free_cmd).result()
        Log.info(free_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, free_msg)

    def tearDown(self):
        Log.info('----------------无需清理环境-----------------------')
        Log.info('-----Opengauss_Function_Tools_gs_ssh_Case0016执行结束-----')
