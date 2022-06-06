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
Case Name   : explain结合分区表的local索引使用
Description :
    1.建分区表
    2.向表中插入数据
    3.创建local索引
    4.explain结合select语句使用，打印执行信息
    5.清理环境
Expect      :
    1.建分区表成功
    2.向表中插入数据成功
    3.创建local索引成功
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
        self.table = 'explain_partition_tab_0001'
        self.index = 'explain_partition_index_0001'
        self.partition_index1 = 'ca_num_index1'
        self.partition_index2 = 'ca_num_index2'
        self.partition_index3 = 'ca_num_index3'

    def test_explain(self):
        self.logger.info('Opengauss_Function_DML_Explain_Case0001 start')
        step = 'step1:建分区表 expect:建分区表成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table};
            create table {self.table} (ca_address varchar(20) not null,
            ca_name varchar(15)  not null,ca_num  integer not null)
            partition by range (ca_num)
            (   
                partition p1 values less than(3),
                partition p2 values less than(6),
                partition p3 values less than(maxvalue)
            )
            enable row movement;''')
        self.logger.info(create_table)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, create_table,
                      "建分区表失败" + step)

        step = 'step2:向表中插入数据 expect:向表中插入数据成功'
        self.logger.info(step)
        insert_data = self.primary_sh.execut_db_sql(f'''
            insert into {self.table} values ('f小区1楼2号','张三',
            generate_series(1,100));''')
        self.logger.info(insert_data)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data,
                      "向表中插入数据失败" + step)

        step = 'step3:创建local索引 expect:创建local索引成功'
        self.logger.info(step)
        create_index = self.primary_sh.execut_db_sql(f'''
            drop index if exists {self.index};
            create index  {self.index} on {self.table} (ca_num) local  
            (
                partition {self.partition_index1},
                partition {self.partition_index2},
                partition {self.partition_index3}
            );''')
        self.logger.info(create_index)
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS, create_index,
                      "创建local索引失败" + step)

        step = 'step4:explain结合select语句使用，打印执行信息' \
               ' expect:打印的执行信息中表的扫描方式为索引扫描'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            set enable_seqscan to off;
            explain select  * from {self.table} where ca_num>20;''')
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
        self.logger.info('Opengauss_Function_DML_Explain_Case0001 finish')
