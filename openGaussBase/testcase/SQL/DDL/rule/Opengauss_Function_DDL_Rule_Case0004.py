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
Case Name   : 非视图的所有者为视图创建rule
Description :
    1.建表1
    2.建表2
    3.向表1,表2中插入数据
    4.为表1创建视图
    5.创建用户
    6.以新建用户的身份为表创建rule
    5.清理环境
Expect      :
    1.建表1成功
    2.建表2成功
    3.向表1,表2中插入数据成功
    4.为表1创建视图成功
    5.为视图创建rule成功
    6.创建失败,合理报错
    5.清理环境成功
History     :
"""

import os
import unittest
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class RULE(unittest.TestCase):
    def setUp(self):
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.log = Logger()
        self.table1 = 't_rule_0004_01'
        self.table2 = 't_rule_0004_02'
        self.rule = 'r_test_0004'
        self.view = 'v_rule_0004'
        self.user = 'u_rule_0004'
        self.encrypt = macro.PASSWD_REPLACE

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

        text = '----step5:创建用户 expect:创建用户成功----'
        self.log.info(text)
        create_user = self.pri_sh.execut_db_sql(
            f'''drop user if exists {self.user};
            create user {self.user} with password '{self.encrypt}';''')
        self.log.info(create_user)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, create_user,
                      '执行失败' + text)

        text = '----step6:以新建用户的身份为表创建rule ' \
               'expect:创建失败,合理报错----'
        self.log.info(text)
        create_rule = self.pri_sh.execut_db_sql(
            f'''create or replace rule {self.rule} as on update to {self.view} 
            do instead update {self.table2} set c_int=20 where c_int<200;;''',
            sql_type=f" -U {self.user} -W {self.encrypt}")
        self.log.info(create_rule)
        self.assertIn(f'ERROR:  must be owner of relation {self.view}', 
                      create_rule, '执行失败' + text)

    def tearDown(self):
        text = '-----step7:清理环境 expect:清理环境成功-----'
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
