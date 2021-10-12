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
'''
--  @date:2020/11/9
--  @testpoint:列存表，执行VACUUM DELTAMERGE语句
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0113开始执行-----------------------------')

    def test_analyze(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
       CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER ,WR_RETURNED_TIME_name varchar(200)) WITH (ORIENTATION = COLUMN);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 插入数据；修改数据后查询系统表
        sql_cmd2 = commonsh.execut_db_sql('''insert into customer_info values (generate_series(1,2000),'a');
        update customer_info set WR_RETURNED_TIME_name='c' where WR_RETURNED_DATE_SK >1000 and WR_RETURNED_DATE_SK<2000;
        select relpages,reltuples from pg_class where relname='customer_info'; ''')
        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.UPDATE_SUCCESS_MSG, sql_cmd2)
        # 执行vacuum DELTAMERGE操作
        sql_cmd3 = commonsh.execut_db_sql('''vacuum DELTAMERGE customer_info;
        select n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='customer_info';''')
        logger.info(sql_cmd3)
        self.assertIn('DELTA MERGE', sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd3 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0113执行结束--------------------------')
