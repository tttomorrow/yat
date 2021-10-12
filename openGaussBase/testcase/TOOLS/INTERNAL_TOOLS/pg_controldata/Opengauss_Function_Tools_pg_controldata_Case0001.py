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
Case Name   : 指定正确的实例目录执行pg_controldata是否成功
Description :
    1.指定正确数据库实例目录执行pg_controldata
    pg_controldata /opt/openGauss_zl/cluster/dn1
    2.信息是否查询成功
Expect      :
    1.pg_controldata执行成功
    2.信息查询成功
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
            '--Opengauss_Function_Tools_pg_controldata_Case0001 start--')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH

    def test_systools(self):
        self.logger.info('-----指定正确数据库实例目录执行pg_controldata-----')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'pg_controldata {macro.DB_INSTANCE_PATH}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find('pg_control version number') > -1)

    def tearDown(self):
        self.logger.info(
            '-Opengauss_Function_Tools_pg_controldata_Case0001 finish-')
