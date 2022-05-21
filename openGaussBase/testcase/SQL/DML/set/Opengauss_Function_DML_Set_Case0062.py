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
--  @testpoint:VACUUM回收空间，添加关键字full，指定列名
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0062开始执行-----------------------------')

    def test_vacuum(self):
        # 建表后查看表的字节大小（建表后，未做任何操作字节为0）；插入数据后再查看表数据
        # 对表进行update操作,通过系统表pg_stat_all_tables查看customer_info表的相关信息,n_dead_tup行更改为1000
        # 对表进行delete操作,通过系统表pg_stat_all_tables查看customer_info表的相关信息，n_dead_tup字段更改为1100（update+delete的行数）
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
                                      CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER,WR_RETURNED_TIME_name varchar(200));
                                      select pg_size_pretty(pg_relation_size('customer_info'));
                                      select n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='customer_info';
                                      insert into customer_info values (generate_series(1,2000),'a');
                                      select pg_size_pretty(pg_relation_size('customer_info'));
                                      select pg_relation_filepath('customer_info');
                                      insert into customer_info values (generate_series(2001,5000),'b');
                                      update customer_info set WR_RETURNED_TIME_name='c' where WR_RETURNED_DATE_SK >4000;
                                      select n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='customer_info';
                                      delete from customer_info where WR_RETURNED_DATE_SK>4900;
                                      select n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='customer_info';''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd1 )
        self.assertIn(constant.UPDATE_SUCCESS_MSG, sql_cmd1)
        self.assertIn(constant.DELETE_SUCCESS_MSG, sql_cmd1)
        # 使用vacuum full机制，表大小发生变化，查询表文件,发生变化,将dead行所占空间归还操作系统,表文件新建
        sql_cmd2 = commonsh.execut_db_sql('''vacuum (full) customer_info(WR_RETURNED_DATE_SK);
                                       select seq_scan,seq_tup_read,n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='customer_info';
                                       select pg_relation_size('customer_info');
                                       select pg_relation_filepath('customer_info);''')

        logger.info(sql_cmd2)
        self.assertIn(constant.VACUUM_SUCCESS_MSG, sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd3 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0062执行结束--------------------------')
