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
Case Type   : analyze
Case Name   : 检测表分区的数据文件
Description :
              1、创建分区表
              2、插入数据
              3、使用analyze分析分区表
              4、删除表
Expect      :
              1、建表成功
              2、插入数据成功
              3、analyze分析分区表完成
              4.删表成功
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

COMMONSH = CommonSH('PrimaryDbUser')
constant = Constant()


class SYS_Operation(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----------Opengauss_Function_DML_Set_Case0107开始执行--------')

    def test_analyze(self):
        self.log.info('步骤1:创建分区表')
        sql_cmd1 = COMMONSH.execut_db_sql('''drop table if exists customer_par;
            create table customer_par(
            wr_returned_date_sk integer ,
            wr_returned_time_sk integer,
            wr_item_sk integer not null,
            wr_refunded_customer_sk  integer
            )
           partition by range(wr_returned_date_sk)
          (
          partition p1 values less than(2452275),
          partition p2 values less than(2452640),
          partition p3 values less than(2453000),
          partition p4 values less than(maxvalue)
          )
          enable row movement;''')
        self.log.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.log.info('步骤2:插入数据后使用analyze分析分区表信息')
        sql_cmd2 = COMMONSH.execut_db_sql('''insert into customer_par values
            (generate_series(2000000,3000000),generate_series(2000000,3000000),
            generate_series(2000000,3000000),generate_series(2000000,3000000));
            analyze verify fast customer_par partition(p1);
            select relname,last_autovacuum,last_analyze from 
            pg_stat_user_tables where relname='customer_par';
            analyze verify fast customer_par partition(p1) cascade;''')
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.ANALYZE_SUCCESS_MSG, sql_cmd2)

    def tearDown(self):
        self.log.info('----------this is teardown-------')
        self.log.info('步骤3:删除表')
        sql_cmd3 = COMMONSH.execut_db_sql('''drop table customer_par 
            cascade;''')
        self.log.info(sql_cmd3)
        self.log.info(
            '-------Opengauss_Function_DML_Set_Case0107执行结束---------')
