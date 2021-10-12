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
Case Type： function
Case Name： pg_stat_get_xact_partition_tuples_deleted(oid)表分区相关的活跃子事务中删除的tuple数。
Create at:  2020/10/9
Descption:  验证增删改查后函数对事务内delete的统计准确性
'''
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
logger = Logger()
class Function(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------StatisticsInfo_xptdeleted_001 start-----------------------------')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()
        self.common = Common('PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        logger.info('----------------------------prepare begin -----------------------------')
        sql_cmd = '''drop table if exists sales;
                      select pg_stat_reset();'''
        self.sh_primy.execut_db_sql(sql_cmd)
        sql_cmd1 = '''begin;
                     CREATE TABLE sales
                     (prod_id NUMBER(6),
                      cust_id NUMBER,
                      time_id DATE,
                      channel_id CHAR(1),
                      promo_id NUMBER(6),
                      quantity_sold NUMBER(3),
                      amount_sold NUMBER(10,2)
                     )
                     PARTITION BY RANGE (time_id)
                     INTERVAL('1 day')
                     ( PARTITION p1 VALUES LESS THAN ('2018-01-01 00:00:00'),
                       PARTITION p2 VALUES LESS THAN ('2019-12-31 00:00:00')
                     );'''
        self.sh_primy.execut_db_sql(sql_cmd1)
    def get_tuples(self):
        logger.info('----------------------------test begin -----------------------------')
        logger.info('--------------testpoint:未插入数据查询是0 ---------------')
        sql_cmd1 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p1';'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        msg1_list = msg1.splitlines()
        self.assertTrue(int(msg1_list[2]) == 0)
        sql_cmd2 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p2';'''
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        msg2_list = msg2.splitlines()
        self.assertTrue(int(msg2_list[2]) == 0)
        logger.info('---------------testpoint:插入数据delete不统计-------------')
        sql_cmd1 = '''INSERT INTO sales VALUES(1, 12, '2017-01-10 00:00:00', 'a', 1, 1, 1);
                      INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'b', 1, 1, 1);
                      INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'c', 1, 1, 1);
                      INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'd', 1, 1, 1);
                      INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'e', 1, 1, 1);
                      INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'f', 1, 1, 1);'''
        self.sh_primy.execut_db_sql(sql_cmd1)
        sql_cmd3 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p1';'''
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        msg3_list = msg3.splitlines()
        self.assertTrue(int(msg3_list[2]) == 0)
        sql_cmd4 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p2';'''
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        msg4_list = msg4.splitlines()
        self.assertTrue(int(msg4_list[2]) == 0)
        logger.info('----------------------------testpoint:验证删除后的统计 -----------------------------')
        logger.info('----------------删除一行 -----------------')
        sql_cmd2 = '''delete  from  sales  where channel_id = 'a';
                      SELECT pg_sleep(1);'''
        self.sh_primy.execut_db_sql(sql_cmd2)
        sql_cmd3 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p1';'''
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        msg3_list = msg3.splitlines()
        self.assertTrue(int(msg3_list[2]) == 1)
        sql_cmd4 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p2';'''
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        msg4_list = msg4.splitlines()
        self.assertTrue(int(msg4_list[2]) == 0)
        logger.info('---------------删除两行一样的 -----------------')
        sql_cmd2 = '''delete  from  sales  where channel_id = 'b';
                      delete  from  sales  where channel_id = 'b';
                      SELECT pg_sleep(1);'''
        self.sh_primy.execut_db_sql(sql_cmd2)
        sql_cmd3 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p1';'''
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        msg3_list = msg3.splitlines()
        self.assertTrue(int(msg3_list[2]) == 1)
        sql_cmd4 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p2';'''
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        msg4_list = msg4.splitlines()
        self.assertTrue(int(msg4_list[2]) == 1)
        logger.info('---------------删除多行 -----------------')
        sql_cmd2 = '''delete  from  sales  where channel_id = 'c';
                        delete  from  sales  where channel_id = 'd';
                        delete  from  sales  where channel_id = 'e';
                        delete  from  sales  where channel_id = 'f';
                        SELECT pg_sleep(1);'''
        self.sh_primy.execut_db_sql(sql_cmd2)
        sql_cmd3 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p1';'''
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        msg3_list = msg3.splitlines()
        self.assertTrue(int(msg3_list[2]) == 1)
        sql_cmd4 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p2';'''
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        msg4_list = msg4.splitlines()
        self.assertTrue(int(msg4_list[2]) == 5)

        logger.info('----------------------------testpoint: 提交事务后，xact的统计自动清0 -----------------------------')
        sql_cmd2 = '''end;
                      SELECT pg_sleep(1);'''
        self.sh_primy.execut_db_sql(sql_cmd2)
        sql_cmd3 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p1';'''
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        msg3_list = msg3.splitlines()
        self.assertTrue(int(msg3_list[2]) == 0)
        sql_cmd4 = '''select pg_stat_get_xact_partition_tuples_deleted(a.oid) from PG_PARTITION a where a.relname = 'p2';'''
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        msg4_list = msg4.splitlines()
        self.assertTrue(int(msg4_list[2]) == 0)

    def tearDown(self):
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        logger.info('----------------------------test end-----------------------------')
        sql_cmd9 = '''drop table sales cascade;'''
        msg9 = self.sh_primy.execut_db_sql(sql_cmd9)
        logger.info(msg9)
        self.assertTrue(msg9.find("DROP TABLE") > -1)
        logger.info('----------------------------StatisticsInfo_xptdeleted_001 finish-----------------------------')