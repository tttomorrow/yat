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
Case Name   : 在openGauss各主机上执行的linux shell命令名:df,du命令
Description :
    1.df命令：显示磁盘空间使用情况
    1.1显示全部文件系统列表
    1.2显示磁盘使用情况
    1.3易读方式列出所有文件系统及其类型
    2.du命令：查看文件和目录对磁盘空间的使用情况
    2.1显示目录中所有文件大小
    2.2显示总计
    2.3显示当前目录下各个子目录所使用的空间
Expect      :
    1.1.显示正确
    1.2.显示正确
    2.3.显示正确
    2.1.显示正确
    2.2.显示正确
    2.3.显示正确
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
        Log.info('------------------显示全部文件系统列表------------------')
        df_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "df -a"'
        Log.info(df_cmd)
        df_msg = self.dbuser_node.sh(df_cmd).result()
        Log.info(df_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, df_msg)

        Log.info('------------------显示磁盘使用情况 ------------------')
        df_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "df -l"'
        Log.info(df_cmd)
        df_msg = self.dbuser_node.sh(df_cmd).result()
        Log.info(df_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, df_msg)
        self.assertIn('Filesystem', df_msg)

        Log.info('-----易读方式列出所有文件系统及其类型-----')
        df_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "df -haT"'
        Log.info(df_cmd)
        df_msg = self.dbuser_node.sh(df_cmd).result()
        Log.info(df_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, df_msg)
        self.assertIn('Filesystem', df_msg)

        Log.info('------------------显示目录中所有文件大小-----------------')
        du_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "du -a"'
        Log.info(du_cmd)
        du_msg = self.dbuser_node.sh(du_cmd).result()
        Log.info(du_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, du_msg)

        Log.info('-----------------显示总计------------------')
        du_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "du -s"'
        Log.info(du_cmd)
        du_msg = self.dbuser_node.sh(du_cmd).result()
        Log.info(du_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, du_msg)

        Log.info('----显示当前目录下各个子目录所使用的空间----')
        du_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "du -hc"'
        Log.info(du_cmd)
        du_msg = self.dbuser_node.sh(du_cmd).result()
        Log.info(du_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, du_msg)

    def tearDown(self):
        Log.info('----------------无需清理环境-----------------------')
        Log.info('-----Opengauss_Function_Tools_gs_ssh_Case0009执行结束-----')
