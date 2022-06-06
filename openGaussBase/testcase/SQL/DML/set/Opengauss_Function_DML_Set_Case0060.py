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
--  @testpoint:vacuum verbose语法测试
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0060开始执行-----------------------------')

    def test_vacuum(self):
        # 建表;查看表的字节大小（建表后，未做任何操作字节为0）
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
                                      CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER,WR_RETURNED_TIME_name varchar(200));
                                      select pg_size_pretty(pg_relation_size('customer_info'));
                                      select n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='customer_info';''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 进行DML操作，查看系统表字段值
        sql_cmd2 = commonsh.execut_db_sql('''insert into customer_info values (generate_series(1,2000),'a');
                                       select pg_size_pretty(pg_relation_size('customer_info'));
                                       select pg_relation_filepath('customer_info');
                                       insert into customer_info values (generate_series(2001,5000),'b');
                                       update customer_info set WR_RETURNED_TIME_name='c' where WR_RETURNED_DATE_SK >4000;
                                       select n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='customer_info';
                                       delete from customer_info where WR_RETURNED_DATE_SK>4900;
                                       select n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='customer_info';''')

        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.UPDATE_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.DELETE_SUCCESS_MSG, sql_cmd2)
        # 使用vacuum freeze
        sql_cmd3 = commonsh.execut_db_sql('''vacuum freeze customer_info;
        select seq_scan,seq_tup_read,n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname = 'customer_info';
        select pg_relation_size('customer_info');
        select pg_relation_filepath('customer_info'); ''')
        logger.info(sql_cmd3)
        self.assertIn(constant.VACUUM_SUCCESS_MSG, sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd4 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0060执行结束--------------------------')
