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
Case Name   : 在opentest各主机上执行的linux shell命令名:wc,head,tail命令
Description :
    1.查看当前工作路径：pwd
    2.创建文件并输入内容
    3.统计输出结果的行数
    4.查找文件的  行数 单词数 字节数 文件名
    5.查看前5行
    6.查看后10行
    7.删除文件
Expect      :
    1.显示路径
    2.文件创建成功
    3.显示行数为13
    4.显示文件a.txt行数 单词数 字节数 文件名正确
    5.正确显示前5行的数据
    6.正确显示后10的数据
    7.文件删除
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
        Log.info('-----Opentest_Function_Tools_gs_ssh_Case0018开始执行-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        Log.info('------------------查看当前路径------------------')
        pwd_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "pwd"'
        Log.info(pwd_cmd)
        pwd_msg = self.dbuser_node.sh(pwd_cmd).result()
        Log.info(pwd_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, pwd_msg)

        Log.info('------------------创建文件并输入内容------------------')
        echo_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "echo \'qazwssxqwertyuiopopasdfghjkl' \
            f'mnbvcxzqazxswedcvfrtggbnhufgghhg   ' \
            f'gftyuytgrgfrggfghvgs_postuninstall -U test909_qm    ' \
            f'--delete-user --delete-groupgs_postuninstall -U   ' \
            f'-X /opt/opentest_qm/package915/opentest.xml  ' \
            f'gs_postuninstall -U test909_qm  ' \
            f'-X /opt/opentest_qm/package915/opentest.xml ' \
            f'gs_postuninstall -U test909_qm   ' \
            f'-X /opt/opentest_qm/package915/opentest.xml  ' \
            f'gs_postuninstall -U test909_qm   ' \
            f'-X /opt/opentest_qm/package915/opentest.xml  ' \
            f'gs_postuninstall -U test909_qm  ' \
            f'-X /opt/opentest_qm/package915/opentest.xml ' \
            f'gs_postuninstall -U test909_qm \'  > a.txt";'
        Log.info(echo_cmd)
        echo_msg = self.dbuser_node.sh(echo_cmd).result()
        Log.info(echo_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, echo_msg)

        Log.info('------------------统计输出结果的行数------------------')
        wc_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "wc -l a.txt"'
        Log.info(wc_cmd)
        wc_msg = self.dbuser_node.sh(wc_cmd).result()
        Log.info(wc_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, wc_msg)

        Log.info('------------------查看前5行------------------')
        head_cmd = f'source {macro.DB_ENV_PATH};' \
            f'head -n 5 a.txt'
        Log.info(head_cmd)
        msg5 = self.dbuser_node.sh(head_cmd).result()
        Log.info(msg5)
        head_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "head -n 5 a.txt"'
        Log.info(head_cmd)
        head_msg = self.dbuser_node.sh(head_cmd).result()
        Log.info(head_msg)
        self.assertIn(msg5, head_msg)

        Log.info('------------------查看后10行------------------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'tail -n 10 a.txt'
        Log.info(check_cmd)
        msg5 = self.dbuser_node.sh(check_cmd).result()
        Log.info(msg5)

        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "tail -n 10 a.txt"'
        Log.info(check_cmd)
        head_msg = self.dbuser_node.sh(check_cmd).result()
        Log.info(head_msg)
        self.assertIn(msg5, head_msg)

    def tearDown(self):
        Log.info('------------------删除文件------------------')
        rm_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "rm -rf a.txt"'
        Log.info(rm_cmd)
        msg = self.dbuser_node.sh(rm_cmd).result()
        Log.info(msg)
        Log.info('----Opentest_Function_Tools_gs_ssh_Case0018执行结束----')
