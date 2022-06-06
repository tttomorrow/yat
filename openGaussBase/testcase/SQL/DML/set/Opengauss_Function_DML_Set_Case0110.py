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
--  @testpoint:事务中，使用analyze语句分析表以及分析列
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0110开始执行-----------------------------')

    def test_analyze(self):
        # 建表并分析不存在的列，合理报错
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
       CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER ,WR_RETURNED_TIME_name varchar(200))WITH (ORIENTATION = COLUMN);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 事务中分析表，合理报错
        sql_cmd2 = commonsh.execut_db_sql('''start transaction;
                                      analyze verbose customer_info;
                                      end;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.ANALYZE_FAIL_MSG, sql_cmd2)
        self.assertIn(constant.ROLLBACK_MSG, sql_cmd2)
        # 事务中分析列，成功
        sql_cmd3 = commonsh.execut_db_sql('''start transaction;
        analyze verbose customer_info(WR_RETURNED_DATE_SK,WR_RETURNED_TIME_name);
        end;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd3)
        self.assertIn(constant.ANALYZE_SUCCESS_MSG, sql_cmd3)
    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd3 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0110执行结束--------------------------')
