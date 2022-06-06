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
Case Type   : 功能测试
Case Name   : reindex DATABASE：重建当前数据库里的所有索引
Description :
    1. 创建分区表及索引
    2. 设置索引unusable，对数据库所有索引进行reindex
    3. 清理环境
Expect      :
    1. 创建成功
    2. 重建成功
    3. 清理成功
History     : 
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('''---Opengauss_Function_DDL_Index_Case0197开始---''')
        cmd = """select CURRENT_CATALOG;"""
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        self.assertTrue(msg.find('ERROR') == -1)
        self.dbname = msg.split('\n')[-2].strip()

    def test_reindex(self):
        self.log.info('--------清理环境--------')
        clear_cmd = '''DROP TABLE if EXISTS tb1 CASCADE;
            DROP TABLE if EXISTS tb2 CASCADE;
            drop index if exists idx1;
            drop index if exists idx2;
            drop index if exists idx3;
            '''
        msg0 = self.commonsh.execut_db_sql(clear_cmd)
        self.log.info(msg0)
        self.assertTrue(msg0.find('ERROR') == -1)

        self.log.info('--------创建表--------')
        cmd1 = '''create table tb1(c_int int,
            c_point point) WITH (ORIENTATION = row);
            create table tb2(c_int int
            ) WITH (ORIENTATION = row) partition by range(c_int)(
            partition p1 values less than (100),
            partition p2 values less than (1000),
            partition p3 values less than (5000),
            partition p4 values less than (10001));
            '''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue(msg1.count('CREATE TABLE') == 2)

        self.log.info('------创建索引----------')
        cmd2 = f'''create index idx1 on tb1(c_int);
            explain select * from tb1 where c_int > 500;
            create index idx2 on tb1 using gist(c_point);
            explain select * from tb1 where c_point <^ point(50,50);
            create index idx3 on tb2(c_int) local (PARTITION p1,PARTITION
            p2,PARTITION p3,PARTITION p4);
            explain select * from tb2 where c_int > 500 group by c_int;
            '''
        msg2 = self.commonsh.execut_db_sql(cmd2)
        self.log.info(msg2)
        self.assertTrue(msg2.find('Bitmap Index Scan on idx1') > -1)
        self.assertTrue(msg2.find('Bitmap Index Scan on idx2') > -1)
        self.assertTrue(msg2.find('Partitioned Bitmap Heap Scan on tb2') > -1)
        self.assertTrue('Partitioned Bitmap Index Scan on idx3' in msg2)

        self.log.info('-------设索引不可用---------')
        cmd3 = '''alter index idx1  UNUSABLE;
            alter index idx2 UNUSABLE;
            alter index idx3 UNUSABLE;
            explain select * from tb1 where c_int > 500;
            explain select * from tb1 where c_point <^ point(50,50);
            explain select * from tb2 where c_int > 500 group by c_int;        
            '''
        msg3 = self.commonsh.execut_db_sql(cmd3)
        self.log.info(msg3)
        self.assertTrue(msg3.count('ALTER INDEX') == 3)
        self.assertTrue(msg3.find('Filter: (c_int > 500)') > -1)
        self.assertTrue("Filter: (c_point <^ '(50,50)'::point)" in msg3)
        self.assertTrue(msg3.find('Filter: (c_int > 500)') > -1)

        self.log.info('-------重建索引---------')
        cmd4 = f'''REINDEX DATABASE {self.dbname};
            explain select * from tb1 where c_int > 500;
            explain select * from tb1 where c_point <^ point(50,50);
            explain select * from tb2 where c_int > 500 group by c_int;
            '''
        msg4 = self.commonsh.execut_db_sql(cmd4)
        self.log.info(msg4)
        self.assertTrue(msg4.find('REINDEX') > -1)

    def tearDown(self):
        clear_cmd = '''DROP TABLE if EXISTS tb1 CASCADE;
            DROP TABLE if EXISTS tb2 CASCADE;
            '''
        self.commonsh.execut_db_sql(clear_cmd)
        self.log.info('''---Opengauss_Function_DDL_Index_Case0197结束---''')