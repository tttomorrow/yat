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
Case Type   : 系统内部使用工具
Case Name   : 查看pscp工具帮助信息
Description :
    1.执行命令查询pscp帮助信息
Expect      :
    1.显示pscp帮助信息成功，共13个选项
History     :
"""

import os
import unittest

from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Tools_Pscp_Case0001 开始执行-')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.pssh_path = os.path.join(
            (os.path.dirname(macro.DB_INSTANCE_PATH)),
            'tool', 'script', 'gspylib', 'pssh', 'bin')

    def test_pscp(self):
        text = '--step1:查询pscp帮助信息;expect:显示pscp帮助信息成功，' \
               '共13个选项--'
        self.log.info(text)
        help_cmd = f" cd {self.pssh_path};" \
                   f"source {macro.DB_ENV_PATH};" \
                   f"python3 pscp --help;"
        self.log.info(help_cmd)
        help_msg = self.PrimaryNode.sh(help_cmd).result()
        self.log.info(help_msg)
        self.log.info('---校验参数存在与否---')
        start_index = help_msg.find('Options:')
        options_list = []
        for i in help_msg[start_index:].split('\n'):
            for j in i.split(' '):
                if len(j) != 0 and j[0] == '-':
                    options_list.append(j)
        self.log.info(options_list)
        parameter = ['--help', '-H', '-h', '-t', '-p', '-o', '-e', '-r', '-v',
                     '-s', '-x', '-i', '-O']
        self.assertEqual(parameter.sort(), options_list.sort(),
                         '执行失败:' + text)

    def tearDown(self):
        self.log.info('-Opengauss_Function_Tools_Pscp_Case0001 执行完成-')
