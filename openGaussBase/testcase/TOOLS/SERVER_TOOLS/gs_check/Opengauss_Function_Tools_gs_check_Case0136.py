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
Case Name   : omm用户检查IO请求
Description :
    1.在非本地模式下检查： gs_check -i CheckIOrequestqueue并交互输入root权限的用户及其密码
    2.在本地模式下检查： gs_check -i CheckIOrequestqueue -L并交互输入root权限的用户及其密码
Expect      :
    1.输入密码完成，检查完成
    2.输入密码完成，检查完成
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-----Opengauss_Function_Tools_gs_check_Case0136_start-----')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.clear_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tool', 'script',
            'gspylib', 'inspection', 'output', 'CheckReport*')
        self.Constant = Constant()

    def test_server_tools(self):
        text = '-----step1:omm用户在非本地模式下检查IO请求;expect:检查完成-----'
        self.log.info(text)
        check_cmd1 = f'''su - {self.dbuserNode.ssh_user} -c "
                    source {macro.DB_ENV_PATH};
                    expect -c \\\"set timeout -1
                    spawn gs_check -i CheckIOrequestqueue
                    expect *]:
                    send {self.rootNode.ssh_user}\\n
                    expect *]:
                    send {self.rootNode.ssh_password}\\n
                    expect eof\\\""'''
        self.log.info(check_cmd1)
        shell_res1 = os.popen(check_cmd1)
        str_res1 = ''.join(shell_res1.readlines())
        self.log.info(str_res1)
        flag = (self.Constant.GS_CHECK_SUCCESS_MSG2[0] in str_res1 or
                self.Constant.GS_CHECK_SUCCESS_MSG2[1] in str_res1) and \
               self.Constant.GS_CHECK_SUCCESS_MSG2[2] in str_res1
        self.assertTrue(flag, '执行失败:' + text)

        text = '-----step2:omm用户在本地模式下检查IO请求;expect:检查完成-----'
        self.log.info(text)
        check_cmd2 = f'''su - {self.dbuserNode.ssh_user} -c "
                   source {macro.DB_ENV_PATH};
                   expect -c \\\"set timeout -1
                   spawn gs_check -i  CheckIOrequestqueue -L
                   expect *]:
                   send {self.rootNode.ssh_user}\\n
                   expect *]:
                   send {self.rootNode.ssh_password}\\n
                   expect eof\\\""'''
        self.log.info(check_cmd2)
        shell_res2 = os.popen(check_cmd2)
        str_res2 = ''.join(shell_res2.readlines())
        self.log.info(str_res2)
        check_result_flag = False
        for single_msg in self.Constant.GS_CHECK_SUCCESS_MSG1:
            if single_msg in str_res2:
                check_result_flag = True
        self.assertTrue(check_result_flag, '执行失败:' + text)

    def tearDown(self):
        text = '----------清理环境----------'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.clear_path};'
        self.log.info(clear_cmd)
        clear_msg = self.rootNode.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.assertEqual('', clear_msg, '执行失败:' + text)
        self.log.info(
            '----Opengauss_Function_Tools_gs_check_Case0136_finish----')
