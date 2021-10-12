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
Case Name   : 
Description :
    1.在当前工作路径下创建文件a.txt,b.txt,c.txt
    2.将以上是三个文件打包到all.tar
    3.查看打包与否成功
    4.删除创建的文档
    5.解压all.tar
    6.查看解压与否成功
    7.删除文档
Expect      :
    1.文件创建成功
    2.打包创建的文件
    3.打包成功
    4.删除创建的文件
    5.解压打包的文件
    6.解压成功
    7.删除文件成功
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
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0020开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        Log.info('-----在当前工作路径下创建文件-----')
        touch_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "touch a.txt";' \
            f'gs_ssh -c "touch b.txt";' \
            f'gs_ssh -c "touch c.txt";'
        Log.info(touch_cmd)
        touch_msg = self.dbuser_node.sh(touch_cmd).result()
        Log.info(touch_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, touch_msg)
        self.assertIn('Successfully execute command on all nodes.', touch_msg)

        Log.info('-----将以上是三个文件打包到all.tar-----')
        tar_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "tar -cvf all.tar a.txt b.txt c.txt";'
        Log.info(tar_cmd)
        tar_msg = self.dbuser_node.sh(tar_cmd).result()
        Log.info(tar_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, tar_msg)
        self.assertIn('SUCCESS', tar_msg)

        Log.info('------------------删除创建的文档------------------')
        rm_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "rm -rf a.txt b.txt c.txt"'
        Log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        Log.info(rm_msg)

        Log.info('------------------解压all.tar------------------')
        tar_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "tar -xvf all.tar"'
        Log.info(tar_cmd)
        tar_cmd = self.dbuser_node.sh(tar_cmd).result()
        Log.info(tar_cmd)
        self.assertIn(self.constant.gs_ssh_success_msg, tar_cmd)
        self.assertIn('SUCCESS', tar_cmd)

        Log.info('------------------查看解压与否成功------------------')
        ls_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ls"'
        Log.info(ls_cmd)
        ls_msg = self.dbuser_node.sh(ls_cmd).result()
        Log.info(ls_msg)
        self.assertIn('all.tar', ls_msg)

    def tearDown(self):
        Log.info('------------------删除文档------------------')
        rm_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "rm -rf a.txt b.txt c.txt all.tar"'
        Log.info(rm_cmd)
        msg = self.dbuser_node.sh(rm_cmd).result()
        Log.info(msg)
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0020执行结束-----')
