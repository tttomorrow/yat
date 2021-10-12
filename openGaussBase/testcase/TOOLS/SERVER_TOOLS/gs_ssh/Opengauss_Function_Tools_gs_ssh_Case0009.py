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
Case Name   : 在openGauss各主机上执行的linux shell命令名: :touch，cp 命令
Description :
    1.查看当前工作路径
    2.在当前目录下创建新的目录
    3.创建文件
    4.查看创建与否成功
    5.复制a.txt到test1目录下
    6.查看是否复制成功
    7.删除文件
    8.删除目录
Expect      :
    1.显示工作路径
    2.创建目录test1成功
    3.创建文件成功
    4.查看成功
    5.复制a.txt到test1目录下成功
    6.查看成功
    7.删除文件
    8.删除目录
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
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0009开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        Log.info('------------------查看当前目录------------------')
        pwd_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "pwd"'
        Log.info(pwd_cmd)
        pwd_msg = self.dbuser_node.sh(pwd_cmd).result()
        Log.info(pwd_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, pwd_msg)

        Log.info('----在当前目录下创建新的目录 ----')
        mkdir_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "mkdir test1"'
        Log.info(mkdir_cmd)
        mkdir_msg = self.dbuser_node.sh(mkdir_cmd).result()
        Log.info(mkdir_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, mkdir_msg)

        Log.info('------------------创建文件------------------')
        touch_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "touch a.txt"'
        Log.info(touch_cmd)
        touch_msg = self.dbuser_node.sh(touch_cmd).result()
        Log.info(touch_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, touch_msg)

        Log.info('------------------查看创建与否成功------------------')
        list_file_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ls"'
        Log.info(list_file_cmd)
        list_file_msg = self.dbuser_node.sh(list_file_cmd).result()
        Log.info(list_file_msg)
        self.assertIn('a.txt', list_file_msg)

        Log.info('------------复制a.txt到test1目录下------------')
        copy_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "cp -a a.txt test1"'
        Log.info(copy_cmd)
        copy_msg = self.dbuser_node.sh(copy_cmd).result()
        Log.info(copy_msg)

        Log.info('------------------查看是否复制成功------------------')
        list_file_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ls test1"'
        Log.info(list_file_cmd)
        list_file_msg = self.dbuser_node.sh(list_file_cmd).result()
        Log.info(list_file_msg)
        self.assertIn('a.txt', list_file_msg)

    def tearDown(self):
        Log.info('------------------删除文件------------------')
        rm_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "rm -rf a.txt"'
        Log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        Log.info(rm_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, rm_msg)

        Log.info('------------------删除目录------------------')
        rm_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "rm -rf test1"'
        Log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        Log.info(rm_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, rm_msg)
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0009执行结束----')
