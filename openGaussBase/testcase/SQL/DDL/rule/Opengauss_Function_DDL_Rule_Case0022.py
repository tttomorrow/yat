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
Case Name   : 为同一个视图创建多个同类型rule,含多条returning语句
Description :
    1.建表1
    2.建表2
    3.向表1,表2中插入数据
    4.为表1创建视图
    5.为同一个视图创建多个同类型rule,含多条returning语句
    6.查询表2数据量
    7.查询表2中c_int<200的数据
    8.通过视图向表1中插入数据,触发rule
    9.清理环境
Expect      :
    1.建表1成功
    2.建表2成功
    3.向表1,表2中插入数据成功
    4.为表1创建视图成功
    5.创建成功
    6.返回表2原始数据量
    7.返回表2原始数据
    8.触发失败,合理报错
    9.清理环境成功
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
        self.table1 = 't_rule_0022_01'
        self.table2 = 't_rule_0022_02'
        self.rule1 = 'r_test_0022_01'
        self.rule2 = 'r_test_0022_02'
        self.view = 'v_rule_0022'

    def test_rule(self):
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        text = '----step1:建表1 expect:建表1成功-----'
        self.log.info(text)
        create_table = self.pri_sh.execut_db_sql(
            f'''drop table if exists {self.table1};
            create table {self.table1}(c_int int);''')
        self.log.info(create_table)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, create_table,
                      '执行失败' + text)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_table,
                      '执行失败' + text)

        text = '----step2:建表2 expect:建表1成功-----'
        self.log.info(text)
        create_table = self.pri_sh.execut_db_sql(
            f'''drop table if exists {self.table2};
            create table {self.table2}(c_int int);''')
        self.log.info(create_table)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, create_table,
                      '执行失败' + text)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_table,
                      '执行失败' + text)

        text = '----step3:向表1,表2中插入数据 ' \
               'expect:向表1,表2中插入数据成功----'
        self.log.info(text)
        insert_data = self.pri_sh.execut_db_sql(
            f'''insert into {self.table1} values(generate_series(1,10000));
            insert into {self.table2} values(generate_series(1,10000));''')
        self.log.info(insert_data)
        self.assertEqual(insert_data.count(self.constant.INSERT_SUCCESS_MSG),
                         2, '执行失败' + text)

        text = '----step4:为表1创建视图 expect:为表1创建视图成功----'
        self.log.info(text)
        create_view = self.pri_sh.execut_db_sql(
            f'''create view {self.view} as select * from {self.table1};''')
        self.log.info(create_view)
        self.assertIn(self.constant.CREATE_VIEW_SUCCESS_MSG, create_view,
                      '执行失败' + text)

        text = '----step5:为同一个视图创建多个同类型rule,含多条returning语句 ' \
               'expect:创建成功'
        self.log.info(text)
        create_rule = self.pri_sh.execut_db_sql(
            f'''create or replace rule {self.rule1} as on insert to 
            {self.view}  do instead insert into {self.table2} 
            values(generate_series(1,100)) returning *;
            create or replace rule {self.rule2} as on insert to {self.view}  
            do instead insert into {self.table2} 
            values(generate_series(1,200)) returning *;''')
        self.log.info(create_rule)
        self.assertEqual(create_rule.count('CREATE RULE'), 2,
                         '执行失败' + text)

        text = '----step6:查询表2数据量 expect:返回表2原始数据量----'
        self.log.info(text)
        select_data = self.pri_sh.execut_db_sql(
            f'''select count(*) from {self.table2};''')
        self.log.info(select_data)
        self.com.equal_sql_mdg(select_data, 'count', '10000', '(1 row)',
                               flag="1")

        text = '----step7:查询表2中c_int<200的数据 expect:返回表2原始数据----'
        self.log.info(text)
        select_data = self.pri_sh.execut_db_sql(
            f'''select * from {self.table2} where c_int<200;''')
        self.log.info(select_data)
        for i in range(0, 200):
            self.assertIn(str(i), select_data, '执行失败' + text)

        text = '----step8:通过视图向表1中插入数据触发rule ' \
               'expect:触发失败,合理报错----'
        self.log.info(text)
        triggering_rule = self.pri_sh.execut_db_sql(
            f'''insert into {self.view} values(generate_series(1,200)) 
            returning *;''')
        self.log.info(triggering_rule)
        self.assertIn('ERROR:  cannot have RETURNING lists in multiple rules',
                      triggering_rule, '执行失败' + text)

    def tearDown(self):
        text = '-----step9:清理环境 expect:清理环境成功-----'
        self.log.info(text)
        clean_environment = self.pri_sh.execut_db_sql(
            f'''drop view {self.view};
            drop table {self.table1};
            drop table {self.table2};''')
        self.log.info(clean_environment)
        self.assertIn(self.constant.DROP_VIEW_SUCCESS_MSG, clean_environment,
                      '执行失败' + text)
        self.assertEqual(clean_environment.count
                         (self.constant.TABLE_DROP_SUCCESS), 2,
                         '执行失败' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
