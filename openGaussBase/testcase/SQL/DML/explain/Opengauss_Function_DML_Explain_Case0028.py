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
"""
Case Type   : explain
Case Name   : explain分析间隔分区表
Description :
    1.建分区表
    2.向分区1中插入数据
    3.向分区2中插入数据
    4.插入没有匹配的分区的数据
    5.explain结合select语句使用,打印执行信息
    6.清理环境
Expect      :
    1.建分区表成功
    2.向分区1中插入数据成功
    3.向分区2中插入数据成功
    4.自动新创建一个分区,并将数据插入该分区
    5.打印执行信息
    6.清理环境成功
History     :
"""

import os
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class SQL(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.table = 'explain_partition_tab_interval_0028'
        self.Constant = Constant()

    def test_explain(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建分区表 expect:建分区表成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table};
            create table {self.table}
            (prod_id number(6),cust_id number,time_id date,channel_id char(1),
             promo_id number(6),quantity_sold number(3),amount_sold 
             number(10,2))
            partition by range (time_id)
            interval('1 day')
            ( partition p1 values less than ('2019-02-01 00:00:00'),
              partition p2 values less than ('2019-02-02 00:00:00')
            );''')
        self.logger.info(create_table)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, create_table,
                      "建分区表失败" + step)

        step = 'step2:向分区1中插入数据 expect:向分区1中插入数据成功'
        self.logger.info(step)
        insert_data1 = self.primary_sh.execut_db_sql(f'''
            insert into {self.table} values(1,12,'2019-01-10 00:00:00','a',1,
            1,1);''')
        self.logger.info(insert_data1)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data1,
                      "向分区1中插入数据失败" + step)

        step = 'step3:向分区2中插入数据 expect:向分区2中插入数据成功'
        self.logger.info(step)
        insert_data2 = self.primary_sh.execut_db_sql(
            f''' insert into {self.table} values(1,12, 
            '2019-02-01 00:00:00','a',1,1,1);''')
        self.logger.info(insert_data2)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data2,
                      "向分区2中插入数据失败" + step)

        step = 'step4:插入没有匹配的分区的数据 ' \
               'expect:自动新创建一个分区,并将数据插入该分区'
        self.logger.info(step)
        insert_data3 = self.primary_sh.execut_db_sql(
            f'''insert into {self.table} values(1,12, 
            '2019-02-05 00:00:00','a',1,1,1);''')
        self.logger.info(insert_data3)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data3,
                      "自动新建分区插入数据失败" + step)

        step = 'step5:explain结合select语句使用,打印执行信息' \
               'expect:打印执行信息'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            explain performance select * from {self.table};''')
        self.logger.info(explain)
        self.assertIn(' Output: prod_id, cust_id, time_id, channel_id, '
                      'promo_id, quantity_sold, amount_sold',
                      explain, "explain无法分析间隔分区表" + step)

    def tearDown(self):
        self.logger.info('清理环境')
        step = 'step6:清理环境 expect:清理环境成功'
        self.logger.info(step)
        de_table = self.primary_sh.execut_db_sql(f'''
            drop table {self.table};''')
        self.logger.info(de_table)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, de_table,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
