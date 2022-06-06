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
Case Type   : rule
Case Name   : 为interval分区表创建rule
Description :
    1.建表1
    2.建表2
    3.为表1创建rule
    4.查看表2数据量
    5.向表1中插入数据
    6.再次查看表2数据量
    7.清理环境
Expect      :
    1.建表1成功
    2.建表2成功
    3.建rule成功
    4.返回0
    5.插入数据成功
    6.返回通过触发rule新增后的数据量
    7.清理环境成功
History     :
"""

import os
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class RULE(unittest.TestCase):
    def setUp(self):
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.com = Common()
        self.constant = Constant()
        self.log = Logger()
        self.table1 = 't_rule_0008_01'
        self.table2 = 't_rule_0008_02'
        self.rule = 'r_test_0008'

    def test_rule(self):
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        text = '----step1:建表1 expect:建表1成功-----'
        self.log.info(text)
        create_table = self.pri_sh.execut_db_sql(
            f'''drop table if exists {self.table1};
            create table {self.table1}(prod_id number(6),cust_id number,
            time_id date,channel_id char(1),promo_id number(6),
            quantity_sold number(3),amount_sold number(10,2))
            partition by range (time_id)
            interval('1 day')
            ( partition  p1 values less than  ('2019-02-01 00:00:00'),
              partition  p2 values less than ('2019-02-02 00:00:00')
            );''')
        self.log.info(create_table)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, create_table,
                      '执行失败' + text)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_table,
                      '执行失败' + text)

        text = '----step2:建表2 expect:建表2成功-----'
        self.log.info(text)
        create_table = self.pri_sh.execut_db_sql(
            f'''drop table if exists {self.table2};
            create table {self.table2}(stu_id number(6),class_id number,
            time_id date,core_id char(1),score_id number(6))
            partition by range (time_id)
            interval('2 day')
            ( partition  p1 values less than  ('2019-02-04 00:00:00'),
              partition  p2 values less than ('2019-02-05 00:00:00')
            );''')
        self.log.info(create_table)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, create_table,
                      '执行失败' + text)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_table,
                      '执行失败' + text)

        text = '----step3:为表1创建rule expect:为表1创建rule成功----'
        self.log.info(text)
        create_rule = self.pri_sh.execut_db_sql(
            f'''create or replace rule {self.rule} as on insert to 
            {self.table1} do also insert into {self.table2} 
            values(1,12,'2019-02-04 00:00:00','a',1);''')
        self.log.info(create_rule)
        self.assertIn('CREATE RULE', create_rule, '执行失败' + text)

        text = '----step4:查看表2数据量 expect:返回0----'
        self.log.info(text)
        select_data = self.pri_sh.execut_db_sql(
            f'''select count(*) from {self.table2};''')
        self.log.info(select_data)
        self.com.equal_sql_mdg(select_data, 'count', '0', '(1 row)', flag="1")

        text = '----step5:向表1中插入数据,触发rule expect:向表1中插入数据成功'
        self.log.info(text)
        insert_data = self.pri_sh.execut_db_sql(f'''insert into {self.table1} 
            values(1,12,'2019-01-10 00:00:00','a',1,1,1);''')
        self.log.info(insert_data)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_data,
                      '执行失败' + text)

        text = '----step6:再次查看表2数据量 expect:返回通过触发rule新增后的数' \
               '据量----'
        self.log.info(text)
        select_data = self.pri_sh.execut_db_sql(
            f'''select count(*) from {self.table2};''')
        self.log.info(select_data)
        self.com.equal_sql_mdg(select_data, 'count', '1', '(1 row)', flag="1")

    def tearDown(self):
        text = '-----step7:清理环境 expect:清理环境成功-----'
        self.log.info(text)
        clean_environment = self.pri_sh.execut_db_sql(
            f'''drop rule {self.rule} on {self.table1};
            drop table {self.table1};
            drop table {self.table2};''')
        self.log.info(clean_environment)
        self.assertEqual(clean_environment.count
                         (self.constant.TABLE_DROP_SUCCESS), 2,
                         '执行失败' + text)
        self.assertIn('DROP RULE', clean_environment, '执行失败' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
