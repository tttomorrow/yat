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
Case Name   : 用户检查防火墙状态（参数i和参数U组合测试，交互输入的用户或密码不正确）
Description :
    1.运行openGauss的用户检查防火墙状态（输入无root权限的用户名）：gs_check -i CheckFirewall -U omm
    2.运行openGauss的用户检查防火墙状态(root权限的用户密码输入错误）：gs_check -i CheckFirewall -U omm
Expect      :
    1.检查失败
    2.检查失败
History     :
"""

import os
import time
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-----Opengauss_Function_Tools_gs_check_Case0303_start-----')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.clear_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tool', 'script',
            'gspylib', 'inspection', 'output', 'CheckReport*')
        self.error_result1 = f'does not have root privileges'
        self.error_result2 = f'ERROR: Verify password failed'
        self.Constant = Constant()

    def test_server_tools1(self):
        text = '-----step1:运行openGauss的用户检查防火墙状态（输入无root权限的用户名）;' \
               'expect:检查失败-----'
        self.log.info(text)
        check_cmd = f'''su - {self.dbuserNode.ssh_user} -c "
                    source {macro.DB_ENV_PATH};
                    expect -c \\\"set timeout -1
                    spawn gs_check -i CheckFirewall -U \
                    {self.dbuserNode.ssh_user}
                    expect *]:
                    send {self.dbuserNode.ssh_user}\\n
                    expect *]:
                    send {self.dbuserNode.ssh_password}\\n
                    expect eof\\\""'''
        self.log.info(check_cmd)
        check_res = self.rootNode.sh(check_cmd).result()
        self.log.info(check_res)
        self.assertIn(self.error_result1, check_res, '执行失败:' + text)

    def test_server_tools2(self):
        text = '-----step2:运行openGauss的用户检查防火墙状态（有root权限的用户密码输入错误）;' \
               'expect:检查失败-----'
        self.log.info(text)
        check_cmd = f'''su - {self.dbuserNode.ssh_user} -c "
                    source {macro.DB_ENV_PATH};
                    expect -c \\\"set timeout 60
                    spawn gs_check -i CheckFirewall -U \
                    {self.dbuserNode.ssh_user}
                    expect *]:
                    send {self.rootNode.ssh_user}\\n
                    expect *]:
                    send {self.rootNode.ssh_user}\\n
                    expect *]:
                    send {self.rootNode.ssh_user}\\n
                    expect *]:
                    send {self.rootNode.ssh_user}\\n
                    expect *]:
                    send {self.rootNode.ssh_user}\\n
                    expect eof\\\""'''
        self.log.info(check_cmd)
        check_res = self.rootNode.sh(check_cmd).result()
        self.log.info(check_res)
        self.assertIn(self.error_result2, check_res, '执行失败:' + text)
        time.sleep(65)

    def tearDown(self):
        text = '----------清理环境----------'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.clear_path};'
        self.log.info(clear_cmd)
        clear_msg = self.rootNode.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.assertEqual('', clear_msg, '执行失败:' + text)
        self.log.info(
            '----Opengauss_Function_Tools_gs_check_Case0303_finish----')
