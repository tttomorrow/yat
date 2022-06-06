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
Case Name   : root用户检查启动项
Description :
    1.root用户进入安装目录下的scriprt目录
    2.在非本地模式下检查： gs_check -i CheckBootItems
    3.在本地模式下检查： gs_check -i CheckBootItems -L
Expect      :
    1.root用户进入安装目录下的scriprt目录
    2.非本地模式下检查失败
    3.本地模式下执行检查完成
History     : 
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-----Opengauss_Function_Tools_gs_check_Case0029start-----')
        self.rootNode = Node('default')
        self.constant = Constant()
        self.SCRIPT_PATH = f'{macro.DB_INSTANCE_PATH}/../tool/script'

    def test_server_tools(self):
        LOG.info('-----root用户在script目录下进行非本地模式下检查启动项-----')
        check_cmd1 = f'cd {self.SCRIPT_PATH};' \
            f' ./gs_check -i CheckBootItems;'
        LOG.info(check_cmd1)
        msg1 = self.rootNode.sh(check_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.constant.GS_CHECK_ERROR_MSG1, msg1)

        LOG.info('-----root用户在script目录下进行本地模式下检查启动项----')
        check_cmd2 = f'cd {self.SCRIPT_PATH};' \
            f' ./gs_check -i CheckBootItems -L;'
        LOG.info(check_cmd2)
        msg2 = self.rootNode.sh(check_cmd2).result()
        LOG.info(msg2)
        check_result_flag = False
        for single_msg in self.constant.GS_CHECK_SUCCESS_MSG1:
            if single_msg in msg2:
                check_result_flag = True
        self.assertTrue(check_result_flag)

    def tearDown(self):
        LOG.info('--------------清理环境---------------')
        clear_cmd = f'rm -rf /tmp/check*;'
        LOG.info(clear_cmd)
        clear_msg = self.rootNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-----------------产生的文件清理完成------------------')
        LOG.info('----Opengauss_Function_Tools_gs_check_Case0029finish----')