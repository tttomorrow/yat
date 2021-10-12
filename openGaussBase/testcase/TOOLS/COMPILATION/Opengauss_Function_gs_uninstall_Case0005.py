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
Case Name   : 执行gs_uninstall -？命令查看帮助信息
Description :
    1.执行gs_uninstall -?
Expect      :
    1.返回帮助信息
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger

Logger = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        Logger.info(
            '----Opengauss_Function_gs_uninstall_Case0005 start----')
        self.rootNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_systools(self):
        Logger.info('------执行gs_uninstall -?命令------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_uninstall -?'
        Logger.info(excute_cmd1)
        msg2 = self.rootNode.sh(excute_cmd1).result()
        Logger.info(msg2)
        msg_list = ['gs_uninstall -? | --help', 'gs_uninstall -V | --version',
                    'gs_uninstall [--delete-data] [-L] [-l LOGFILE]',
                    '-L                                Only uninstall local',
                    '-l                                Path of log file',
                    '-?, --help                        Show help information',
                    '-V, --version                     Show version']
        for content in msg_list:
            self.assertTrue(msg2.find(content) > -1)

    def tearDown(self):
        Logger.info(
            '---Opengauss_Function_gs_uninstall_Case0005 finish---')
