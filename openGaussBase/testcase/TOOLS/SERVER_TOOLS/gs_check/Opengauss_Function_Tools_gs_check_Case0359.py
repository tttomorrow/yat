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
Case Name   : omm用户进行升级前巡检场景检查（upgrade）
Description :
     升级前巡检场景检查：gs_check -e upgrade -U omm
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
            '----Opengauss_Function_Tools_gs_check_Case0359_开始----')
        self.dbuser_node = Node('dbuser')
        self.root_node = Node('default')
        self.clear_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tool', 'script',
            'gspylib', 'inspection', 'output', 'CheckReport*')
        self.Constant = Constant()

    def test_server_tools1(self):
        text = '-------step1:omm用户进行升级前巡检场景检查;expect:检查完成-------'
        self.log.info(text)
        check_cmd = f'''su - {self.dbuser_node.ssh_user} -c "
                    source {macro.DB_ENV_PATH};
                    expect -c \\\"set timeout -1
                    spawn gs_check -e upgrade -U {self.dbuser_node.ssh_user}
                    expect *]:
                    send {self.root_node.ssh_user}\\n
                    expect *]:
                    send {self.root_node.ssh_password}\\n
                    expect eof\\\""'''
        self.log.info(check_cmd)
        shell_res = os.popen(check_cmd)
        str_res = ''.join(shell_res.readlines())
        self.log.info(str_res)
        flag = (self.Constant.GS_CHECK_SUCCESS_MSG2[0] in str_res or
                self.Constant.GS_CHECK_SUCCESS_MSG2[1] in str_res) and \
               self.Constant.GS_CHECK_SUCCESS_MSG2[2] in str_res
        self.assertTrue(flag, '执行失败:' + text)

    def tearDown(self):
        text = '----------清理环境----------'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.clear_path};'
        self.log.info(clear_cmd)
        clear_msg = self.root_node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.assertEqual('', clear_msg, '执行失败:' + text)
        self.log.info('---Opengauss_Function_Tools_gs_check_Case0359finis---')
