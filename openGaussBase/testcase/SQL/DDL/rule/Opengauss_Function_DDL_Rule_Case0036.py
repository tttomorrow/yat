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
Case Name   : 创建delete类型rule,do指定instead nothing
Description :
    1.建表1
    2.建表2
    3.向表1,表2中插入数据
    4.查询表2数据量
    5.为表1创建rule
    6.删除表1数据,触发rule
    7.再次查询表2数据量
    8.清理环境
Expect      :
    1.建表1成功
    2.建表2成功
    3.向表1,表2中插入数据成功
    4.返回原始数据量
    5.创建rule成功
    6.不删除表2数据
    7.返回原始数据量
    8.清理环境成功
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
        self.table1 = 't_rule_0036_01'
        self.table2 = 't_rule_0036_02'
        self.rule = 'r_test_0036'

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

        text = '----step4:查询表2的数据量 expect:返回原始数据量----'
        self.log.info(text)
        select_data = self.pri_sh.execut_db_sql(
            f'''select count(*) from {self.table2};''')
        self.log.info(select_data)
        self.com.equal_sql_mdg(select_data, 'count', '10000', '(1 row)',
                               flag="1")

        text = '----step5:为表1创建rule expect:创建rule成功-----'
        self.log.info(text)
        create_rule = self.pri_sh.execut_db_sql(
            f'''create or replace rule {self.rule} as on delete to 
            {self.table1} do instead nothing;''')
        self.log.info(create_rule)
        self.assertIn('CREATE RULE', create_rule, '执行失败' + text)

        text = '----step6:删除表1数据,触发rule expect:不删除表2数据----'
        self.log.info(text)
        delete_data = self.pri_sh.execut_db_sql(
            f'''delete from {self.table1};''')
        self.log.info(delete_data)
        self.assertIn('DELETE 0', delete_data, '执行失败' + text)

        text = '----step7:查询表2的数据量 expect:返回原始数据量----'
        self.log.info(text)
        select_data = self.pri_sh.execut_db_sql(
            f'''select count(*) from {self.table2};''')
        self.log.info(select_data)
        self.com.equal_sql_mdg(select_data, 'count', '10000', '(1 row)',
                               flag="1")

    def tearDown(self):
        text = '-----step8:清理环境 expect:清理环境成功-----'
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
