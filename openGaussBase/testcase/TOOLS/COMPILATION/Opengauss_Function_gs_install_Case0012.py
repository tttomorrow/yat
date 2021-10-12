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
Case Type   : tools
Case Name   : 执行gs_install -？命令查看帮助信息
Description :
    1.执行gs_install -?
Expect      :
    1.返回帮助信息
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger

Logger = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        Logger.info(
            '----Opengauss_Function_gs_install_Case0012 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_systools(self):
        Logger.info('------执行gs_install -V命令------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_install -?'
        Logger.info(excute_cmd1)
        msg2 = self.userNode.sh(excute_cmd1).result()
        Logger.info(msg2)
        msg_list = ['gs_install -? | --help', 'gs_install -V | --version',
                    'gs_install -X XMLFILE', '-X', '-l', '-?, --help',
                    '-V, --version', '--gsinit-parameter="PARAMETER"',
                    '--dn-guc="PARAMETER"',
                    '--alarm-component=ALARMCOMPONENT', '--time-out=SECS', ]
        for content in msg_list:
            self.assertTrue(msg2.find(content) > -1)

    def tearDown(self):
        Logger.info('---Opengauss_Function_gs_install_Case0012 finish---')
