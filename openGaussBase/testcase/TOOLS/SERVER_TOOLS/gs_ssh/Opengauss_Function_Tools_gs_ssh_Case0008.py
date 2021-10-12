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
Case Name   : 在openGauss各主机上执行的linux shell命令名:touch,mv命令
Description :
    1.创建文件
    2.查看创建与否成功
    3.将文件test1重命名为test1.txt
    4.查看是否重命名成功
    5.将文件test1.txt移动到dn1目录中
    6.查看是否移动成功
    7.删除文件
Expect      :
    1.创建文件test1
    2.创建成功
    3.重命名文件
    4.重命名成功
    5.移动文件到dn1目录下
    6.移动成功
    7.删除文件
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
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0008开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        Log.info('------------------创建文件------------------')
        touch_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "touch test1"'
        Log.info(touch_cmd)
        touch_msg = self.dbuser_node.sh(touch_cmd).result()
        Log.info(touch_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, touch_msg)

        Log.info('------将文件test1重命名为test1.txt------')
        mv_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "mv test1 test1.txt"'
        Log.info(mv_cmd)
        mv_msg = self.dbuser_node.sh(mv_cmd).result()
        Log.info(mv_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, mv_msg)

        Log.info('------------------查看是否重命名成功------------------')
        list_file_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ls"'
        Log.info(list_file_cmd)
        list_file_msg = self.dbuser_node.sh(list_file_cmd).result()
        Log.info(list_file_msg)
        self.assertIn('test1.txt', list_file_msg)

        Log.info('-------------将文件test1.txt移动到dn1目录中-------------')
        mv_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "mv test1.txt {macro.DB_INSTANCE_PATH}"'
        Log.info(mv_cmd)
        mv_msg = self.dbuser_node.sh(mv_cmd).result()
        Log.info(mv_msg)

        Log.info('------------------查看是否移动成功------------------')
        list_file_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ls {macro.DB_INSTANCE_PATH}"'
        Log.info(list_file_cmd)
        list_file_msg = self.dbuser_node.sh(list_file_cmd).result()
        Log.info(list_file_msg)
        self.assertIn('test1.txt', list_file_msg)

    def tearDown(self):
        Log.info('------------------删除文件------------------')
        rm_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "rm -rf {macro.DB_INSTANCE_PATH}/test1.txt"'
        Log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        Log.info(rm_msg)
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0008执行结束----')
