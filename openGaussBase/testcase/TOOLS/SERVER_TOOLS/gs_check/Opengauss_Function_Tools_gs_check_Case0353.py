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
Case Name   : 在本地进行例行巡检场景检查（inspect）
Description :
     例行巡检场景检查：gs_check -e inspect -L
Expect      :
     检查完成
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
            '-----Opengauss_Function_Tools_gs_check_Case0353_开始-----')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.clear_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tool', 'script',
            'gspylib', 'inspection', 'output', 'CheckReport*')
        self.Constant = Constant()

    def test_server_tools1(self):
        text = '--------step1:在本地进行例行巡检场景检查;expect:检查完成---------'
        self.log.info(text)
        check_cmd = f'''su - {self.dbuserNode.ssh_user} -c "
                       source {macro.DB_ENV_PATH};
                       expect -c \\\"set timeout -1
                       spawn gs_check -e inspect -L
                       expect *]:
                       send {self.rootNode.ssh_user}\\n
                       expect *]:
                       send {self.rootNode.ssh_password}\\n
                       expect eof\\\""'''
        self.log.info(check_cmd)
        shell_res = os.popen(check_cmd)
        self.log.info(shell_res)
        str_res = ''.join(shell_res.readlines())
        self.log.info(str_res)
        check_result_flag = False
        for single_msg in self.Constant.GS_CHECK_SUCCESS_MSG1:
            if single_msg in str_res:
                check_result_flag = True
        self.assertTrue(check_result_flag, '执行失败' + text)

    def tearDown(self):
        text = '----------清理环境----------'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.clear_path};'
        self.log.info(clear_cmd)
        clear_msg = self.rootNode.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.assertEqual('', clear_msg, '执行失败:' + text)
        self.log.info(
            '-------Opengauss_Function_Tools_gs_check_Case0353_结束------')
