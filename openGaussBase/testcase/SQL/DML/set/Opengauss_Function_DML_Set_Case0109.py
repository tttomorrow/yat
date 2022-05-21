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
--  @testpoint:使用analyze分析不存在的表名和列名，合理报错
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0109开始执行-----------------------------')

    def test_analyze(self):
        # 使用analyze分析不存在的表，合理报错
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_1;
        analyze verbose customer_1;''')
        logger.info(sql_cmd1)
        self.assertIn('ERROR:  relation "customer_1" does not exist', sql_cmd1)
        # 建表并分析不存在的列，合理报错
        sql_cmd2 = commonsh.execut_db_sql('''drop table if exists customer_info;
       CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER ,WR_RETURNED_TIME_name varchar(200))WITH (ORIENTATION = COLUMN);
       analyze verbose customer_info(WR_RETURNED_DATE_SK1,WR_RETURNED_TIME_name);''')
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd2)
        self.assertIn('ERROR:  column "wr_returned_date_sk1" of relation "customer_info" does not exist', sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd3 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0109执行结束--------------------------')
