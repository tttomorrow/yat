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
Case Name   : 用户检查防火墙状态（参数i和参数U组合测试，交互输入的用户或密码不正确）
Description :
    1.运行openGauss的用户检查防火墙状态（输入无root权限的用户名）：gs_check -i CheckFirewall -U omm
    2.运行openGauss的用户检查防火墙状态(root权限的用户密码输入错误）：gs_check -i CheckFirewall -U omm
Expect      :
    1.检查失败
    2.检查失败
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()

class Tools(unittest.TestCase):
    def setUp(self):
        logger.info('--------------Opengauss_Function_Tools_gs_check_Case0303start-------------------')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------运行openGauss的用户检查防火墙状态（输入无root权限的用户名）------------------')
        logger.info(vars(self.dbuserNode))
        check_cmd1 = f'''
                        source {macro.DB_ENV_PATH}
                        expect <<EOF
                        set timeout -1
                        spawn gs_check -i CheckFirewall -U {self.dbuserNode.ssh_user}
                        expect "*]:"
                        send "{self.dbuserNode.ssh_user}\r"
                        expect "*]:"
                        send "{self.rootNode.db_password}\r"
                        expect eof
                        '''
        logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        logger.info(msg1)
        self.assertIn('does not have root privileges',msg1)

    def test_server_tools2(self):
        logger.info('------------------运行openGauss的用户检查防火墙状态(root权限的用户密码输入错误）------------------')
        logger.info(vars(self.dbuserNode))
        check_cmd2 = f'''
                        source {macro.DB_ENV_PATH}
                        expect <<EOF
                        set timeout -1
                        spawn gs_check -i CheckFirewall -U {self.dbuserNode.ssh_user}
                        expect "*]:"
                        send "{self.rootNode.ssh_user}\r"
                        expect "*]:"
                        send "{self.rootNode.db_host}\r"
                        expect "*]:"
                        send "{self.rootNode.db_host}\r"
                        expect "*]:"
                        send "{self.rootNode.db_host}\r"
                        expect "*]:"
                        send "{self.rootNode.db_host}\r"
                        expect eof
                        '''
        logger.info(check_cmd2)
        msg2 = self.dbuserNode.sh(check_cmd2).result()
        logger.info(msg2)
        self.assertIn('ERROR: Verify password failed',msg2)

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_check_Case0303finish------------------')
