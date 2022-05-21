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
'''
--  @testpoint:COMPACT和PARTITION参数同时使用，合理报错
'''
import sys
import unittest
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0068开始执行-----------------------------')

    def test_vacuum(self):
        # 创建分区表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists test_part;
     create table test_part (id int, name varchar)partition by range(id)
    (partition p1 values less than (10),
    partition p2 values less than (20),
    partition p3 values less than (30),
    partition p4 values less than (40),
    partition p5 values less than (50));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 查看表的字节大小（建表后，未做任何操作字节为0）；插入数据，查看表的字节大小，有变化
        # 分别修改数据，n_dead_tup行更改为3；删除数据，n_dead_tup字段更改为4（update+delete的行数）
        sql_cmd2 = commonsh.execut_db_sql('''select pg_size_pretty(pg_relation_size('test_part'));
        select n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='test_part';
        insert into test_part values(5,'a'),(15,'b'),(25,'c'),(35,'d'),(45,'e');
        select pg_size_pretty(pg_relation_size('test_part'));
        select pg_relation_filepath('test_part');
        update test_part set name ='cici' where id>20;
        delete from test_part where id>40;
        select n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='test_part';
        ''')
        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.DELETE_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.UPDATE_SUCCESS_MSG, sql_cmd2 )
        # 使用vacuum full机制,合理报错;通过系统表pg_stat_all_tables查看test_part表的相关信息，n_dead_tup字段依旧为4
        sql_cmd3 = commonsh.execut_db_sql('''vacuum full COMPACT test_part partition(p4);
        select n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='test_part';''')
        logger.info(sql_cmd3)
        self.assertIn('ERROR:  COMPACT can not be used with PARTITION', sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd4 = commonsh.execut_db_sql('''drop table test_part;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0068执行结束--------------------------')
