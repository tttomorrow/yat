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
Case Type   : 并行查询
Case Name   : 设置参数query_dop=1与query_dop=3时，查询成功
Description :
        1.创建列存表
        2.插入数据
        3.执行analyze
        4.设置query_dop=1并执行带limit的查询语句
        5.设置query_dop=3并执行带limit的查询语句
        6.清理环境
Expect      :
        1.创建列存表成功
        2.插入数据成功
        3.执行analyze成功
        4.设置query_dop=1并执行带limit的查询语句，查询成功
        5.设置query_dop=3并执行带limit的查询语句，查询成功，相对于query_dop=1
        查询较慢，但是不会卡住
        6.清理环境成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

commonsh = CommonSH('PrimaryDbUser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-------Opengauss_Function_Tools_Query_Dop_Case0038start-------')
        self.constant = Constant()
        self.Primary_User_Node = Node('PrimaryDbUser')

    def test_enable_beta_features(self):
        self.log.info('---步骤1:创建列存表---')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists column_table;
            create table column_table (id int,a int,b char(20)) 
            with (orientation = column);
            drop table if exists column_table_01;
            create table column_table_01 (id int,a int,b char(20)) 
            with (orientation = column);''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.log.info('---步骤2:插入数据---')
        sql_cmd = commonsh.execut_db_sql('''insert into column_table\
            select id,id % 10,'foo'from generate_series(1, 1000000) id;
            insert into column_table_01 select id,id % 10,'foo'from \
            generate_series(1, 1000000) id;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        self.log.info('---步骤3:执行analyze---')
        sql_cmd = commonsh.execut_db_sql('''analyze column_table;
            analyze column_table_01; ''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.ANALYZE_SUCCESS_MSG, sql_cmd)
        self.log.info('---步骤4:设置query_dop=1并执行查询语句---')
        sql_cmd = commonsh.execut_db_sql('''set query_dop=1;\
        select table_002.id column_006,table_002.b column_007,\
        table_003.column_004 column_008,table_003.column_005 column_009\
        from column_table table_002 inner \
        join (select table_001.id column_001,table_001.a column_002,\
        table_002.a column_003,table_002.b column_004,\
        table_001.b column_005 from column_table table_002\
        full outer join column_table_01 table_001\
        on table_002.a = table_001.id) table_003\
        on table_002.a = table_003.column_001 limit 10;''')
        self.log.info(sql_cmd)
        self.assertIn('10 rows', sql_cmd)
        self.log.info('---步骤5:设置query_dop=3并执行查询语句---')
        sql_cmd = commonsh.execut_db_sql('''set query_dop=3;\
        select table_002.id column_006,table_002.b column_007,\
        table_003.column_004 column_008,table_003.column_005 column_009\
        from column_table table_002 inner \
        join (select table_001.id column_001,table_001.a column_002,\
        table_002.a column_003,table_002.b column_004,\
        table_001.b column_005 from column_table table_002\
        full outer join column_table_01 table_001\
        on table_002.a = table_001.id) table_003\
        on table_002.a = table_003.column_001 limit 10;''')
        self.log.info(sql_cmd)
        self.assertIn('10 rows', sql_cmd)

    def tearDown(self):
        self.log.info('---步骤6:清理环境---')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists column_table;
            drop table if exists column_table_01;''')
        self.log.info(sql_cmd)
        self.log.info(
            '------Opengauss_Function_Tools_Query_Dop_Case0038finish-----')
