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
Case Name   : 为视图创建delete类型的无条件instead规则,规则使用returning语句,
              不使用returning语句触发
Description :
    1.建表1
    2.建表2
    3.向表1,表2中插入数据
    4.为表1创建视图
    5.为视图创建rule,使用returning语句
    6.查询表2的数据量
    7.通过视图删除表1数据,触发rule
    8.查询表1数据量
    9.再次查询表2数据量
    10.清理环境
Expect      :
    1.建表1成功
    2.建表2成功
    3.向表1,表2中插入数据成功
    4.为表1创建视图成功
    5.为视图创建rule成功
    6.返回原始数据量
    7.删除表2数据成功,不返回删除的表2数据
    8.返回表1原始数据量
    9.返回表2通过触发rule删除数据后的数据量
    10.清理环境成功
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
        self.table1 = 't_rule_0019_01'
        self.table2 = 't_rule_0019_02'
        self.rule = 'r_test_0019'
        self.view = 'v_rule_0019'

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
            f'''insert into {self.table1} values(generate_series(600,1000));
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

        text = '----step5:为视图创建rule,使用returning语句 ' \
               'expect:为视图创建rule成功-----'
        self.log.info(text)
        create_rule = self.pri_sh.execut_db_sql(
            f'''create or replace rule {self.rule} as on delete to {self.view} 
            do instead delete from {self.table2} where c_int < 500 returning *;
            ''')
        self.log.info(create_rule)
        self.assertIn('CREATE RULE', create_rule, '执行失败' + text)

        text = '----step6:查询表2的数据量 expect:返回原始数据量----'
        self.log.info(text)
        select_data = self.pri_sh.execut_db_sql(
            f'''select count(*) from {self.table2};''')
        self.log.info(select_data)
        self.com.equal_sql_mdg(select_data, 'count', '10000', '(1 row)',
                               flag="1")

        text = '----step7:通过视图删除表1数据,触发rule ' \
               'expect:删除表2数据成功,不返回删除的表2数据----'
        self.log.info(text)
        delete_data = self.pri_sh.execut_db_sql(
            f'''delete from {self.view};''')
        self.log.info(delete_data)
        self.assertIn(self.constant.DELETE_SUCCESS_MSG, delete_data,
                      '执行失败' + text)

        text = '----step8:查询表1的数据量 expect:返回表1原始数据量----'
        self.log.info(text)
        select_data = self.pri_sh.execut_db_sql(
            f'''select count(*) from {self.table1};''')
        self.log.info(select_data)
        self.com.equal_sql_mdg(select_data, 'count', '401', '(1 row)',
                               flag="1")

        text = '----step9:再次查询表2的数据量 ' \
               'expect:返回表2通过触发rule删除数据后的数据量----'
        self.log.info(text)
        select_data = self.pri_sh.execut_db_sql(
            f'''select count(*) from {self.table2};''')
        self.log.info(select_data)
        self.com.equal_sql_mdg(select_data, 'count', '9501', '(1 row)',
                               flag="1")

    def tearDown(self):
        text = '-----step10:清理环境 expect:清理环境成功-----'
        self.log.info(text)
        clean_environment = self.pri_sh.execut_db_sql(
            f'''drop rule {self.rule} on {self.view};
            drop view {self.view};
            drop table {self.table1};
            drop table {self.table2};''')
        self.log.info(clean_environment)
        self.assertIn(self.constant.DROP_VIEW_SUCCESS_MSG, clean_environment,
                      '执行失败' + text)
        self.assertEqual(clean_environment.count
                         (self.constant.TABLE_DROP_SUCCESS), 2,
                         '执行失败' + text)
        self.assertIn('DROP RULE', clean_environment, '执行失败' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
