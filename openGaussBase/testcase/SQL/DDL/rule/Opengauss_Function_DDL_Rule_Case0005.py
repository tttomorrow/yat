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
Case Name   : 同一表创建多个UPDATE类型rule,按照规则名称的字母顺序触发
Description :
    1.建表1
    2.建表2
    3.为表1创建rule1
    4.为表1创建rule2
    5.向表1插入数据,触发rule1,rule2
    6.查询表2的数据
    7.清理环境
Expect      :
    1.建表1成功
    2.建表2成功
    3.为表1创建rule1成功
    4.为表1创建rule2成功
    5.向表1插入数据成功
    6.返回插入的数据
    7.清理环境成功
History     :
"""

import os
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class RULE(unittest.TestCase):
    def setUp(self):
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.log = Logger()
        self.table1 = 't_rule_0005_01'
        self.table2 = 't_rule_0005_02'
        self.rule1 = 'r_test_0005_01'
        self.rule2 = 'r_test_0005_02'
        self.view = 'v_rule_0005'

    def test_rule(self):
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        text = '----step1:建表1 expect:建表1成功-----'
        self.log.info(text)
        create_table = self.pri_sh.execut_db_sql(
            f'''drop table if exists {self.table1};
            create table {self.table1}(c_int int,c1_int int);''')
        self.log.info(create_table)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, create_table,
                      '执行失败' + text)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_table,
                      '执行失败' + text)

        text = '----step2:建表2 expect:建表1成功-----'
        self.log.info(text)
        create_table = self.pri_sh.execut_db_sql(
            f'''drop table if exists {self.table2};
            create table {self.table2}(c_int int,c1_int int);''')
        self.log.info(create_table)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, create_table,
                      '执行失败' + text)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_table,
                      '执行失败' + text)

        text = '----step3:为表1创建rule1 expect:为表1创建rule1成功----'
        self.log.info(text)
        create_rule = self.pri_sh.execut_db_sql(
            f'''create or replace rule {self.rule1} as on insert to 
            {self.table1} do also insert into {self.table2} select 1,count(*) 
            from {self.table2};''')
        self.log.info(create_rule)
        self.assertIn('CREATE RULE', create_rule, '执行失败' + text)

        text = '----step4:为表1创建rule2 expect:为表1创建rule1成功----'
        self.log.info(text)
        create_rule = self.pri_sh.execut_db_sql(
            f'''create or replace rule {self.rule2} as on insert to 
            {self.table1} do also insert into {self.table2} select 2,count(*) 
            from {self.table2};''')
        self.log.info(create_rule)
        self.assertIn('CREATE RULE', create_rule, '执行失败' + text)

        text = '----step5:向表1插入数据,触发rule1,rule2 ' \
               'expect:向表1插入数据成功----'
        self.log.info(text)
        insert_data = self.pri_sh.execut_db_sql(
            f'''insert into {self.table1} values(12,1);''')
        self.log.info(insert_data)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_data,
                      '执行失败' + text)

        text = '----step6:查询表2的数据 expect:返回插入的数据----'
        self.log.info(text)
        select_data = self.pri_sh.execut_db_sql(
            f'''select * from {self.table2};''')
        self.log.info(select_data)
        self.assertIn('2 |      1', select_data, '执行失败' + text)

    def tearDown(self):
        text = '-----step7:清理环境 expect:清理环境成功-----'
        self.log.info(text)
        clean_environment = self.pri_sh.execut_db_sql(
            f'''drop rule {self.rule1} on {self.table1};
            drop rule {self.rule2} on {self.table1};
            drop table {self.table1};
            drop table {self.table2};''')
        self.log.info(clean_environment)
        self.assertEqual(clean_environment.count('DROP RULE'), 2,
                         '执行失败' + text)
        self.assertEqual(clean_environment.count
                         (self.constant.TABLE_DROP_SUCCESS), 2,
                         '执行失败' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
