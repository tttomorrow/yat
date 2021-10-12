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
Case Type   : 常量与宏
Case Name   : CURRENT_SCHEMA无效值测试
Description :
    1.分别执行select current_schemas;select current_schema('');
Expect      :
    1.合理报错
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class ConstantsMacros(unittest.TestCase):
    def setUp(self):
        logger.info(
            '------------------------Opengauss_Function_DDL_Constants_Macros_Case0006开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_current_schema(self):
        sql_cmd1 = commonsh.execut_db_sql('''select current_schemas;
                                           select current_schema('');''')
        logger.info(sql_cmd1)
        self.assertIn('ERROR:', sql_cmd1)

    # 清理环境:no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info(
            '------------------------Opengauss_Function_DDL_Constants_Macros_Case0006执行结束--------------------------')
