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
--  @testpoint:使用analyze收集分区表的统计信息
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0096开始执行-----------------------------')

    def test_analyze(self):
        # 创建表并插入数据
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_par;
CREATE TABLE customer_par
(
WR_RETURNED_DATE_SK       INTEGER ,
WR_RETURNED_TIME_SK       INTEGER,
WR_ITEM_SK                INTEGER NOT NULL,
WR_REFUNDED_CUSTOMER_SK   INTEGER
)
PARTITION BY RANGE(WR_RETURNED_DATE_SK)
(
PARTITION P1 VALUES LESS THAN(2452275),
PARTITION P2 VALUES LESS THAN(2452640),
PARTITION P3 VALUES LESS THAN(2453000),
PARTITION P4 VALUES LESS THAN(MAXVALUE)
)
ENABLE ROW MOVEMENT;
insert into customer_par values(generate_series(2000000,3000000),generate_series(2000000,3000000),generate_series(2000000,3000000),generate_series(2000000,3000000));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd1)
        # 使用ANALYZE直接加表名；查看上一次手动ANALYZE的时间
        # 使用ANALYZE VERBOSE语句更新统计信息，并输出表的相关信息
        sql_cmd2 = commonsh.execut_db_sql('''ANALYZE customer_par;
        select relname,last_autovacuum,last_analyze from pg_stat_user_tables where relname='customer_par';
        ANALYZE verbose customer_par;
        ''')
        logger.info(sql_cmd2)
        self.assertIn(constant.ANALYZE_SUCCESS_MSG, sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd3 = commonsh.execut_db_sql('''drop table customer_par;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0096执行结束--------------------------')
