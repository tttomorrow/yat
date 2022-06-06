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
Case Name   : explain结合视图使用
Description :
    1.建表
    2.向表中插入数据
    3.建视图
    4.explain结合select语句使用,打印执行信息
    5.清理环境
Expect      :
    1.建表成功
    2.向表中插入数据成功
    3.建视图成功
    4.打印执行信息
    5.清理环境
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
        self.table = 'explain_view_0032'
        self.view = 'select_view_0032'
        self.Constant = Constant()

    def test_explain(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建表 expect:建表成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table};
            create table {self.table}(col1 int,col2 int);''')
        self.logger.info(create_table)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, create_table,
                      "建表失败" + step)

        step = 'step2:向表中插入数据 expect:向表中插入数据成功'
        self.logger.info(step)
        insert_data = self.primary_sh.execut_db_sql(f'''
            insert into  {self.table} values(1,1),(2,2);''')
        self.logger.info(insert_data)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data,
                      "向表中插入数据失败" + step)

        step = 'step3:建视图 expect:建视图成功'
        self.logger.info(step)
        create_view = self.primary_sh.execut_db_sql(f'''
            create view {self.view} as select * from {self.table};''')
        self.logger.info(create_view)
        self.assertIn(self.Constant.CREATE_VIEW_SUCCESS_MSG, create_view,
                      "建视图失败" + step)

        step = 'step4:explain结合select语句使用,打印执行信息' \
               'expect:打印执行信息'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            explain performance select * from {self.view};''')
        self.logger.info(explain)
        self.assertIn(f'Output: {self.table}.col1, {self.table}.col2',
                      explain, "explain无法分析视图" + step)

    def tearDown(self):
        step = 'step5:清理环境 expect:清理环境成功'
        self.logger.info(step)
        de_environment = self.primary_sh.execut_db_sql(f'''
            drop view {self.view};
            drop table {self.table};''')
        self.logger.info(de_environment)
        self.assertTrue(self.Constant.DROP_VIEW_SUCCESS_MSG in de_environment
                        and self.Constant.DROP_TABLE_SUCCESS in de_environment
                        , "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
