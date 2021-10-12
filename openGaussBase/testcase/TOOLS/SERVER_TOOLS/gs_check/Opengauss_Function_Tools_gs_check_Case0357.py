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
Case Name   : 在本地执行安装场景检查（install)
Description :
     在本地执行安装场景检查：gs_check -e install -L
Expect      :
     检查完成
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Tools_gs_check_Case0357start---')
        self.dbusernode = Node('dbuser')
        self.rootnode = Node('default')
        self.constant = Constant()

    def test_server_tools1(self):
        self.log.info('-------------在本地执行安装场景检查---------------')
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            expect <<EOF
            set timeout -1
            spawn gs_check -e install -L 
            expect "*]:"
            send "{self.rootnode.ssh_user}\r"
            expect "*]:"
            send "{self.rootnode.ssh_password}\r"
            expect eof\n''' + "EOF"

        self.log.info(check_cmd1)
        check_msg1 = self.dbusernode.sh(check_cmd1).result()
        check_result = check_msg1.count('[RST]')
        self.log.info(check_result)
        self.assertEqual(check_result, 40, '在本地执行安装场景检查不通过')

    def tearDown(self):
        self.log.info('--------------无需清理环境-------------------')
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0357finish--')
