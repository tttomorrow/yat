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
Case Type   : tools
Case Name   : 执行gs_uninstall -V命令查看版本信息
Description :
    1.执行gs_uninstall -V
Expect      :
    1.返回版本信息
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
            '----Opengauss_Function_gs_uninstall_Case0004 start----')
        self.rootNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_systools(self):
        Logger.info('------执行gs_uninstall -V命令------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_uninstall -V'
        Logger.info(excute_cmd1)
        msg2 = self.rootNode.sh(excute_cmd1).result()
        Logger.info(msg2)
        self.assertTrue(msg2.find('compiled at') > -1)

    def tearDown(self):
        Logger.info(
            '---Opengauss_Function_gs_uninstall_Case0004 finish---')
