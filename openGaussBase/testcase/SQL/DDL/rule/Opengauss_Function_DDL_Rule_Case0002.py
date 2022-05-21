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
Case Name   : 非表的所有者为表创建rule,合理报错
Description :
    1.建表1
    2.建表2
    3.创建用户
    4.以新建用户的身份为表创建rule
    5.清理环境
Expect      :
    1.建表1成功
    2.建表2成功
    3.创建用户成功
    4.创建失败,合理报错
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
        self.table1 = 't_rule_0002_01'
        self.table2 = 't_rule_0002_02'
        self.rule = 'r_test_0002'
        self.user = 'u_rule_0002'
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

        text = '----step3:创建用户 expect:创建用户成功----'
        self.log.info(text)
        create_user = self.pri_sh.execut_db_sql(
            f'''drop user if exists {self.user};
            create user {self.user} with password '{self.encrypt}';''')
        self.log.info(create_user)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, create_user,
                      '执行失败' + text)

        text = '----step4:以新建用户的身份为表创建rule ' \
               'expect:创建失败,合理报错----'
        self.log.info(text)
        create_rule = self.pri_sh.execut_db_sql(
            f'''create or replace rule {self.rule} as on insert to 
            {self.table1} do also insert into {self.table2} 
            values(generate_series(1,10000));''', sql_type=f" -U {self.user} "
            f"-W {self.encrypt}")
        self.log.info(create_rule)
        self.assertIn(f'ERROR:  must be owner of relation {self.table1}',
                      create_rule, '执行失败' + text)

    def tearDown(self):
        text = '-----step5:清理环境 expect:清理环境成功-----'
        self.log.info(text)
        clean_environment = self.pri_sh.execut_db_sql(
            f'''drop table {self.table1};
            drop table {self.table2};
            drop user {self.user};''')
        self.log.info(clean_environment)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, clean_environment,
                      '执行失败' + text)
        self.assertEqual(clean_environment.count
                         (self.constant.TABLE_DROP_SUCCESS), 2,
                         '执行失败' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
