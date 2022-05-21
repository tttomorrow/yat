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
'''
--  @testpoint:设置所属模式,语法中不使用to或者=，合理报错
'''
import sys
import unittest
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0127开始执行-----------------------------')

    def test_reset(self):
        # 设置所属模式,合理报错
        sql_cmd1 = commonsh.execut_db_sql('''show CURRENT_SCHEMA;
                                       drop schema if exists my_schema1 cascade;
                                       create schema my_schema1;
                                       set session CURRENT_SCHEMA !=my_schema1;
                                       set session CURRENT_SCHEMA to = my_schema1;''')
        logger.info(sql_cmd1)
        self.assertIn('"$user",public', sql_cmd1)
        self.assertIn(constant.CREATE_SCHEMA_SUCCESS_MSG, sql_cmd1)
        self.assertIn('ERROR:  syntax error', sql_cmd1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd2 = commonsh.execut_db_sql('''drop schema my_schema1 cascade;''')
        logger.info('------------------------Opengauss_Function_DML_Set_Case0127执行结束--------------------------')
