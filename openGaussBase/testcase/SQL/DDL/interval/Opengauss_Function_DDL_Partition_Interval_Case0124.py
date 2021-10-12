"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Type   : 功能测试
Case Name   : interval分区,MODIFY PARTITION设置索引不可用
Description :
    1. 创建分区表及local索引
    2. 设置索引不可用
    3. 重建索引
Expect      :
    1. 创建成功
    2. 设置成功，查询不走索引
    3. 恢复成功，查询走了索引
History     :
"""
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0124开始')

    def test_alter_index(self):
        self.log.info('---步骤1 创建interval分区表,建索引,插入数据---')
        cmd0 = '''drop index if exists idx9;
            drop table if exists pt99;
            set enable_seqscan = off;
            
            create table pt99(col_1 smallint, col_2 char(30),
            col_3 int, col_4 date, col_5 boolean,
            col_6 nchar(30), col_7 float)
            partition by range (col_4) interval ('1 month')
            (
            partition pt99_p1 values less than ('2020-03-01'),
            partition pt99_p2 values less than ('2020-04-01'),
            partition pt99_p3 values less than ('2020-05-01')
            );
            
            create index idx9 on pt99(col_4) local
            (
                partition col_4_index1,
                partition col_4_index2,
                partition col_4_index3
            );'''
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.assertTrue(msg0.find('CREATE TABLE') > -1)
        self.assertTrue(msg0.find('CREATE INDEX') > -1)

        cmd2 = '''begin
                      for i in 1..10000 loop
                         insert into pt99(col_4) select date '2019-12-31' + i;
                      end loop;
                  end;'''
        msg2 = self.commonsh.execut_db_sql(cmd2)
        self.log.info(msg2)
        self.assertTrue(msg2.find('ANONYMOUS BLOCK EXECUTE') > -1)

        self.log.info('--步骤2、3 设置索引不可用后再重建索引--')
        mode = ['unusable local indexes', 'rebuild unusable local indexes']
        info = 'Partitioned Bitmap Index Scan on idx9'

        def set_index(status):
            cmd3 = f'alter table pt99 modify partition pt99_p3 {status};'
            msg3 = self.commonsh.execut_db_sql(cmd3)
            self.log.info(msg3)
            return msg3

        def check_index():
            cmd4 = f'''explain select col_4 from pt99 
                where col_4 < '2020-05-01' and col_4 > '2020-04-01';'''
            msg4 = self.commonsh.execut_db_sql(cmd4)
            self.log.info(msg4)
            return msg4

        set_index(mode[0])
        self.assertTrue(check_index().find(info) == -1)
        set_index(mode[1])
        self.assertTrue(check_index().find(info) > -1)

    def tearDown(self):
        self.commonsh.execut_db_sql('''drop index if exists idx9;
            drop table if exists pt99;
            set enable_seqscan = on;''')
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0124结束')