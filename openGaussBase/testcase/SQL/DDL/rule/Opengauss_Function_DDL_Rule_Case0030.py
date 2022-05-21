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
Case Name   : 为不存在的表创建rule,合理报错
Description :
    1.建表
    2.为不存在的表创建rule
    3.清理环境
Expect      :
    1.建表1成功
    2.创建失败,合理报错
    3.清理环境成功
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
        self.table1 = 't_table_rule_0030_01'
        self.table2 = 't_table_rule_0030_02'
        self.rule = 'r_test_0030'

    def test_rule(self):
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        text = '----step1:建表 expect:建表成功-----'
        self.log.info(text)
        create_table = self.pri_sh.execut_db_sql(
            f'''drop table if exists {self.table1};
            create table {self.table1}(c_int int);''')
        self.log.info(create_table)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, create_table,
                      '执行失败' + text)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_table,
                      '执行失败' + text)

        text = '----step2:为不存在的表创建rule expect:创建失败,合理报错----'
        self.log.info(text)
        create_rule = self.pri_sh.execut_db_sql(
            f'''create or replace rule {self.rule} as on insert to 
            {self.table2} do also insert into {self.table1} 
            values(generate_series(1,10000));''')
        self.log.info(create_rule)
        s = f'ERROR:  relation "{self.table2}" does not exist'
        self.assertIn(s, create_rule, '执行失败' + text)

    def tearDown(self):
        text = '-----step3:清理环境 expect:清理环境成功-----'
        self.log.info(text)
        clean_environment = self.pri_sh.execut_db_sql(
            f'''drop table {self.table1};''')
        self.log.info(clean_environment)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, clean_environment,
                      '执行失败' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
