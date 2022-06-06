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
Case Name   : explain按顺序使用参数,参数仅限analyse|analyse,verbose,performance
Description :
    1.建表
    2.向表中插入数据
    3.explain考虑参数顺序,使用analyse,打印执行信息
    4.explain考虑参数顺序,使用analyze,打印执行信息
    5.explain考虑参数顺序,使用verbose,打印执行信息
    6.explain考虑参数顺序,使用performance,打印执行信息
    7.explain考虑参数顺序,使用costs,打印执行信息
    8.清理环境
Expect      :
    1.建表成功
    2.向表中插入数据成功
    3.打印执行信息
    4.打印执行信息
    5.打印执行信息
    6.打印执行信息
    7.报错提示语法错误
    8.清理环境成功
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
        self.table = 'explain_order_params_0034'
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
            insert into {self.table} values(1,1),(2,2);''')
        self.logger.info(insert_data)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data,
                      "向表中插入数据失败" + step)

        step = 'step3:explain考虑参数顺序,使用analyse,打印执行信息' \
               'expect:打印执行信息'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            explain analyse select * from {self.table};''')
        self.logger.info(explain)
        self.assertIn('actual time', explain, "打印信息不正确" + step)

        step = 'step4:explain考虑参数顺序,使用analyze,打印执行信息' \
               'expect:打印执行信息'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            explain analyze select * from {self.table};''')
        self.logger.info(explain)
        self.assertIn('actual time', explain, "打印信息不正确" + step)

        step = 'step5:explain考虑参数顺序,使用verbose,打印执行信息' \
               'expect:打印执行信息'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            explain verbose select * from {self.table};''')
        self.logger.info(explain)
        self.assertIn(' Output: col1, col2', explain, "打印信息不正确" + step)

        step = 'step6:explain考虑参数顺序,使用performance,打印执行信息' \
               'expect:打印执行信息'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            explain performance select * from {self.table};''')
        self.logger.info(explain)
        self.assertTrue('actual time' in explain and 'Output:' in explain
                        and 'Buffers:' in explain and 'CPU:' in explain,
                        "打印信息不正确" + step)

        step = 'step7:explain考虑参数顺序,使用costs,打印执行信息' \
               'expect:报错提示语法错误'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            explain costs select * from {self.table};''')
        self.logger.info(explain)
        self.assertIn('ERROR:  syntax error at or near "costs"', explain,
                      "执行结果错误" + step)

    def tearDown(self):
        self.logger.info('清理环境')
        step = 'step8:清理环境 expect:清理环境成功'
        self.logger.info(step)
        de_table = self.primary_sh.execut_db_sql(f'''
            drop table {self.table};''')
        self.logger.info(de_table)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, de_table,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
