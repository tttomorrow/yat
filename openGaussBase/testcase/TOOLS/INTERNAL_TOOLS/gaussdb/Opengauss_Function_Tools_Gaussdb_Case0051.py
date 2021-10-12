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
Case Name   : 执行gaussdb使用参数--describe-config查看配置参数的描述是否成功
Description :
    1.执行gaussdb查看配置参数命令
    gaussdb --describe-config
    2.查看配置参数的描述是否显示成功
Expect      :
    1.执行gaussdb查看配置参数命令成功
    2.配置参数的描述显示成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_Gaussdb_Case0051 start--')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_systools(self):
        self.logger.info('--------执行gaussdb查看配置参数命令--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH}; gaussdb --describe-config'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(
            msg1.find('Sets how binary values are to be encoded in XML') > -1)

    def tearDown(self):
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0051 finish-')
