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
Case Name   : 在openGauss各主机上执行的linux shell命令名:cat命令
Description :
    1.查看当前工作路径
    2.创建文件并输入内容
    3.查看文件
    4.将文件a.txt,b.txt合并到c.txt文件
    5.查看是否合并成功
    6.删除文件：gs_ssh -c "rm -rf a.txt"
                gs_ssh -c "rm -rf b.txt"
                gs_ssh -c "rm -rf c.txt"
Expect      :
    1.显示工作路径成功
    2.创建文件并输入内容成功
    3.创建成功
    4.合并文件成功
    5.查看成功
    6.删除成功
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

        Log.info('------------------创建文件并输入内容 ------------------')
        echo_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "echo \'qazwssx\' > a.txt"; ' \
            f' gs_ssh -c "echo \'qwertyuiop\' > b.txt" '
        Log.info(echo_cmd)
        echo_msg = self.dbuser_node.sh(echo_cmd).result()
        Log.info(echo_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, echo_msg)

        Log.info('------------------查看文件------------------')
        ls_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "ls"'
        Log.info(ls_cmd)
        ls_msg = self.dbuser_node.sh(ls_cmd).result()
        Log.info(ls_msg)
        self.assertIn('a.txt', ls_msg)
        self.assertIn('b.txt', ls_msg)

        Log.info('-----将文件a.txt,b.txt合并到c.txt文件-----')
        cat_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "cat a.txt b.txt > c.txt"'
        Log.info(cat_cmd)
        cat_msg = self.dbuser_node.sh(cat_cmd).result()
        Log.info(cat_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, cat_msg)

        Log.info('-----------------查看是否合并成功------------------')
        cat_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "cat c.txt"'
        Log.info(cat_cmd)
        cat_msg = self.dbuser_node.sh(cat_cmd).result()
        Log.info(cat_msg)
        self.assertIn('qwertyuiop', cat_msg)

        Log.info('------------------删除文件-----------------')
        rm_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "rm -rf a.txt";' \
            f'gs_ssh -c "rm -rf b.txt";' \
            f'gs_ssh -c "rm -rf c.txt"'
        Log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        Log.info(rm_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, rm_msg)

    def tearDown(self):
        Log.info('----------------无需清理环境-----------------------')
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0009执行结束----')
