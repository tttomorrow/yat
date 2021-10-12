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
Case Name   : 在openGauss各主机上执行的linux shell命令名：pwd命令
Description : gs_ssh -c "pwd"
Expect      : 显示当前路径
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
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0006开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        Log.info('---列出主备机当前目录下相关文件夹包含的文件---')
        list_file_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "pwd"'
        Log.info(list_file_cmd)
        msg = self.dbuser_node.sh(list_file_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.gs_ssh_success_msg, msg)

    def tearDown(self):
        Log.info('----------------无需清理环境-----------------------')
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0006执行结束----')
