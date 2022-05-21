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
Case Name   : explain分析列表分区表
Description :
    1.建分区表
    2.向分区1中插入数据
    3.向分区2中插入数据
    4.插入没有匹配的分区的数据
    5.新建分区,重新插入数据到新建的分区
    6.explain结合select语句使用,打印执行信息
    7.清理环境
Expect      :
    1.建分区表成功
    2.向分区1中插入数据成功
    3.向分区2中插入数据成功
    4.报错提示对应分区不存在
    5.新建分区成功,插入数据成功
    6.打印执行信息
    7.清理环境成功
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
        self.table = 'explain_partition_tab_list_0029'
        self.Constant = Constant()

    def test_explain(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建分区表 expect:建分区表成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table};
            create table {self.table}(col1 int,col2 int)
            partition by list(col1)
            (
                partition p1 values (2000),
                partition p2 values (3000),
                partition p3 values (4000),
                partition p4 values (5000)
            );''')
        self.logger.info(create_table)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, create_table,
                      "建分区表失败" + step)

        step = 'step2:向分区1中插入数据 expect:向分区1中插入数据成功'
        self.logger.info(step)
        insert_data1 = self.primary_sh.execut_db_sql(f'''
            insert into {self.table} values(2000, 2000);''')
        self.logger.info(insert_data1)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data1,
                      "向分区1中插入数据失败" + step)

        step = 'step3:向分区2中插入数据 expect:向分区2中插入数据成功'
        self.logger.info(step)
        insert_data2 = self.primary_sh.execut_db_sql(f'''
            insert into {self.table} values(3000, 3000);''')
        self.logger.info(insert_data2)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data2,
                      "向分区2中插入数据失败" + step)

        step = 'step4:插入没有匹配的分区的数据 expect:报错提示对应分区不存在'
        self.logger.info(step)
        insert_data3 = self.primary_sh.execut_db_sql(f'''
            insert into {self.table} values(6000, 6000);''')
        self.logger.info(insert_data3)
        self.assertIn('ERROR:  inserted partition key does not map to any '
                      'table partition', insert_data3, "分区错误" + step)

        step = 'step5:新建分区,重新插入数据到新建的分 expect:插入数据成功'
        self.logger.info(step)
        insert_data4 = self.primary_sh.execut_db_sql(f'''
            alter table {self.table} add partition p5 
            values (6000);
            insert into  {self.table} VALUES(6000, 6000);''')
        self.logger.info(insert_data4)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data4,
                      "插入数据失败" + step)

        step = 'step6:explain结合select语句使用,打印执行信息 ' \
               'expect:打印执行信息'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            explain performance select * from {self.table};''')
        self.logger.info(explain)
        self.assertIn('Output: col1, col2', explain,
                      "explain无法分析间隔分区表" + step)

    def tearDown(self):
        self.logger.info('清理环境')
        step = 'step7:清理环境 expect:清理环境成功'
        self.logger.info(step)
        de_table = self.primary_sh.execut_db_sql(f'''
            drop table {self.table};''')
        self.logger.info(de_table)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, de_table,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
