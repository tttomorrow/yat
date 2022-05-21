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
Case Name   : 在openGauss各主机上执行的linux
            shell命令名:whereis,find,locate,which命令
Description :
    1.查找locate程序相关文件
    2.在当前目录查找 以.log结尾的文件
    3.查看ls命令是否存在
    4.查看which
Expect      :
    1.显示正确
    2.显示正确
    3.显示正确
    4.显示正确
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
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0017开始执行-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        Log.info('-------步骤1.查找locate程序相关文件---------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "whereis locate"'
        Log.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.gs_ssh_success_msg, msg)
        self.assertIn('locate:', msg)

        Log.info('-------步骤2.在当前目录查找 以.log结尾的文件-------')
        find_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "find ./ -name \'*.log\'"'
        Log.info(find_cmd)
        find_msg = self.dbuser_node.sh(find_cmd).result()
        Log.info(find_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, find_msg)

        Log.info('-------步骤3.查看ls命令是否存在-------')
        which_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "which ls"'
        Log.info(which_cmd)
        which_msg = self.dbuser_node.sh(which_cmd).result()
        Log.info(which_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, which_msg)

        Log.info('-------步骤4.查看which-------')
        which_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "which which"'
        Log.info(which_cmd)
        which_msg = self.dbuser_node.sh(which_cmd).result()
        Log.info(which_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, which_msg)

    def tearDown(self):
        Log.info('----------------无需清理环境-----------------------')
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0017执行结束----')
