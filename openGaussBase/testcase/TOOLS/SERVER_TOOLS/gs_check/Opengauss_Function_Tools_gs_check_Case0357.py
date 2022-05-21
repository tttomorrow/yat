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
Case Name   : 在本地执行安装场景检查（install)
Description :
     在本地执行安装场景检查：gs_check -e install -L
Expect      :
     检查完成
History     :
"""

import os
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-----Opengauss_Function_Tools_gs_check_Case0357_start-----')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.clear_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tool', 'script',
            'gspylib', 'inspection', 'output', 'CheckReport*')
        self.Constant = Constant()

    def test_server_tools1(self):
        text = '-----step1:在本地执行安装场景检查;expect:检查完成-----'
        self.log.info(text)
        check_cmd = f'''su - {self.dbuserNode.ssh_user} -c "
                    source {macro.DB_ENV_PATH};
                    expect -c \\\"set timeout -1
                    spawn gs_check -e install -L
                    expect *]:
                    send {self.rootNode.ssh_user}\\n
                    expect *]:
                    send {self.rootNode.ssh_password}\\n
                    expect eof\\\""'''
        self.log.info(check_cmd)
        shell_res = os.popen(check_cmd)
        str_res = ''.join(shell_res.readlines())
        self.log.info(str_res)
        check_result = str_res.count('[RST]')
        self.log.info(check_result)
        self.assertLessEqual(check_result, 40, '在本地执行安装场景检查不通过')

    def tearDown(self):
        text = '----------清理环境----------'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.clear_path};'
        self.log.info(clear_cmd)
        clear_msg = self.rootNode.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.assertEqual('', clear_msg, '执行失败:' + text)
        self.log.info(
            '----Opengauss_Function_Tools_gs_check_Case0357_finish----')
