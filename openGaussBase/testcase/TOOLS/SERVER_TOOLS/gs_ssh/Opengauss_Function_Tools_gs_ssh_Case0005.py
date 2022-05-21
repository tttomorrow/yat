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
Case Name   : 在openGauss各主机上执行的linux shell命令名: ls命令
Description :
    1.gs_ssh -c "ls"
    2.gs_ssh -c "ls -a"
    3.gs_ssh -c "ls -a /home"
    4.gs_ssh -c "ls -l /home"
Expect      :
    1.列出主备机当前目录下相关文件夹包含的文件
    2.列出当前目录所有文件，包含以.开始的隐藏文件
    3.列出home目录所有文件，包含以.开始的隐藏文件
    4.列出home目录下除文件名之外，还将文件的权限、
    所有者、文件大小等信息详细列出来
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
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0005开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        Log.info('----列出主备机当前目录下相关文件夹包含的文件----')
        list_file_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ls" '
        Log.info(list_file_cmd)
        msg = self.dbuser_node.sh(list_file_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.gs_ssh_success_msg, msg)

    def test_server_tools2(self):
        Log.info('----列出当前目录所有文件，包含以.开始的隐藏文件----')
        list_file_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ls -a"'
        Log.info(list_file_cmd)
        msg = self.dbuser_node.sh(list_file_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.gs_ssh_success_msg, msg)

    def test_server_tools3(self):
        Log.info('----列出home目录所有文件，包含以.开始的隐藏文件----')
        list_file_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ls -a /home"'
        Log.info(list_file_cmd)
        msg = self.dbuser_node.sh(list_file_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.gs_ssh_success_msg, msg)

    def test_server_tools4(self):
        Log.info('---列出home目录下除文件名之外，还将文件的权限所有者、文件大小等信息详细列出来----')
        list_file_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ls -l /home"'
        Log.info(list_file_cmd)
        msg = self.dbuser_node.sh(list_file_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.gs_ssh_success_msg, msg)

    def tearDown(self):
        Log.info('----------------无需清理环境-----------------------')
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0005执行结束----')
