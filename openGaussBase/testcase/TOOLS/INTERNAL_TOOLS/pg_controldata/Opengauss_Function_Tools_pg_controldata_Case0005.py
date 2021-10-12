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
Case Name   : pg_controldata使用-?查看帮助信息
Description :
    1.使用-V参数执行pg_controldata
    pg_controldata -?
    2.信息是否查询成功
    3.使用--help参数执行pg_controldata
    pg_controldata --help
    4.信息是否查询成功
Expect      :
    1.使用-?参数执行pg_controldata成功
    2.信息查询成功
    3.使用-help参数执行pg_controldata成功
    4.信息查询成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '----Opengauss_Function_Tools_pg_controldata_Case0005 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_systools(self):
        self.logger.info('--------查看帮助信息--------')
        help_msg = ['-V, --version  output version information, then exit',
                    '-?, --help     show this help, then exit']
        excute_cmd1 = f'source {self.DB_ENV_PATH};pg_controldata -?'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        for content in (help_msg):
            self.logger.info(content)
            self.assertTrue(msg1.find(content) > -1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};pg_controldata --help'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        for content in (help_msg):
            self.logger.info(content)
            self.assertTrue(msg1.find(content) > -1)

    def tearDown(self):
        self.logger.info(
            '----Opengauss_Function_Tools_pg_controldata_Case0005 finish----')
