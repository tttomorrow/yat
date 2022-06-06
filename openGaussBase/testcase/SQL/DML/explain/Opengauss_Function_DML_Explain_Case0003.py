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
Case Name   : explain结合建行存表btree索引使用
Description :
    1.建行存表
    2.向表中插入数据
    3.创建btree索引
    4.explain结合select语句使用，打印执行信息
    5.清理环境
Expect      :
    1.建行存表成功
    2.向表中插入数据成功
    3.创建btree索引成功
    4.打印的执行信息中表的扫描方式为索引扫描
    5.清理环境成功
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class SQL(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.dbuserNode = Node('PrimaryDbUser')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.table = 'explain_row_tab_0003'
        self.index = 'explain_row_index_0003'

    def test_explain(self):
        self.logger.info('Opengauss_Function_DML_Explain_Case0003 start')
        step = 'step1:建行存表 expect:建行存表成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table};
            create table {self.table} 
            (name varchar(10),stu_id varchar(5) not null, score int,num int );
            ''')
        self.logger.info(create_table)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, create_table,
                      "建行存表失败" + step)

        step = 'step2:向表中插入数据 expect:向表中插入数据成功'
        self.logger.info(step)
        insert_data = self.primary_sh.execut_db_sql(f'''
            insert into {self.table} values('数学','01',90,
            generate_series(1,500));''')
        self.logger.info(insert_data)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data,
                      "向表中插入数据失败" + step)

        step = 'step3:创建btree索引 expect:创建btree索引成功'
        self.logger.info(step)
        create_index = self.primary_sh.execut_db_sql(f'''
            drop index if exists {self.index};
            create index {self.index} on {self.table} using btree (num);''')
        self.logger.info(create_index)
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS, create_index,
                      "创建btree索引失败" + step)

        step = 'step4:explain结合select语句使用，打印执行信息' \
               ' expect:打印的执行信息中表的扫描方式为索引扫描'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            set enable_seqscan to off;
            explain select  * from {self.table}  where num > 100;''')
        self.logger.info(explain)
        self.assertIn('Index Scan ', explain, "打印信息错误" + step)

    def tearDown(self):
        step = 'step5:清理环境 expect:清理环境成功'
        self.logger.info(step)
        de_index_table = self.primary_sh.execut_db_sql(f'''
            drop table {self.table};''')
        self.logger.info(de_index_table)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, de_index_table,
                      "执行失败" + step)
        self.logger.info('Opengauss_Function_DML_Explain_Case0003 finish')
