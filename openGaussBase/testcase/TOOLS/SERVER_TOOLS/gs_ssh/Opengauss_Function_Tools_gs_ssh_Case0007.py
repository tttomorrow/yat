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
Case Name   : 在openGauss各主机上执行的linux shell命令名:pwd,mkdir,rm命令
Description :
    1.查看当前工作路径
    2.在当前目录下创建新的目录test01
    3.查看创建是否成功
    4.删除目录
Expect      :
    1.显示工作路径成功
    2.查看成功
    3.创建成功
    4.删除目录成功
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
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0007开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.primarynode = Node('PrimaryDbUser')

    def test_server_tools1(self):
        Log.info('----列出主备机当前目录下相关文件夹包含的文件----')
        list_file_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "pwd"'
        Log.info(list_file_cmd)
        list_file_msg = self.dbuser_node.sh(list_file_cmd).result()
        Log.info(list_file_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, list_file_msg)

        Log.info('----在当前目录下创建新的目录test01----')
        mkdir_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "mkdir test01"'
        Log.info(mkdir_cmd)
        mkdir_msg = self.dbuser_node.sh(mkdir_cmd).result()
        Log.info(mkdir_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, mkdir_msg)

        Log.info('------------------查看创建是否成功------------------')
        list_file_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ls"'
        Log.info(list_file_cmd)
        list_file_msg = self.primarynode.sh(list_file_cmd).result()
        Log.info(list_file_msg)
        self.assertIn('test01', list_file_msg)

    def tearDown(self):
        Log.info('------------------删除目录------------------')
        rm_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "rm -rf test01"'
        Log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        Log.info(rm_msg)
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0007执行结束----')
