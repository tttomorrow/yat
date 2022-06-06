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
Case Name   : 使用pg_table_is_visible函数查询表在搜索路径中是否可见
Description :
    1.一个表所在的模式是public
    2.一个表所在的模式在搜索路径中，并且在前面的搜索路径中没有同名的表
    3.一个表所在的模式在搜索路径中，并且在前面的搜索路径中有同名的表
Expect      :
    1. 这个表是可见的
    2. 这个表是可见的
    3. 表不可见
History     : 
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('''---
            Opengauss_Function_Innerfunc_Pg_Table_Is_Visible_Case0001开始---''')

    def test_scheme(self):
        self.log.info('''------------1.查询不带模式(属于pubic)的表------------''')
        create_tb1 = '''drop table if exists no_scheme;
            create table no_scheme(id int, name varchar(20));
            select oid from pg_class where relname='no_scheme';
            '''
        msg0 = self.commonsh.execut_db_sql(create_tb1)
        self.log.info(msg0)
        oid1 = msg0.splitlines()[-2].strip()
        query1 = f'''select pg_table_is_visible({oid1});
            drop table if exists no_scheme;
            '''
        msg1 = self.commonsh.execut_db_sql(query1)
        self.log.info(msg1)
        self.assertTrue(msg1.splitlines()[-4].strip() == 't')

        self.log.info('''----------------2.查询带模式的表-------------------''')
        create_tb2 = f'''drop table if exists s_1.tbone; 
            drop schema if exists s_1;
            create schema s_1;
            create table s_1.tbone(id int, name varchar(20));
            select oid from pg_class where relname='tbone';
            '''
        msg2 = self.commonsh.execut_db_sql(create_tb2)
        self.log.info(msg2)
        oid2 = msg2.splitlines()[-2].strip()
        self.assertTrue(msg2.find('CREATE TABLE') > -1)
        self.log.info('''-------未设置搜索路径直接查询-------''')
        query2 = f'''select pg_table_is_visible({oid2});'''
        msg3 = self.commonsh.execut_db_sql(query2)
        self.log.info(msg3)
        self.assertTrue(msg3.splitlines()[-2].strip() == 'f')
        self.log.info('''-------设置搜索路径后查询-----------''')
        query3 = f'''set search_path to s_1, public;
            select pg_table_is_visible({oid2});'''
        msg4 = self.commonsh.execut_db_sql(query3)
        self.log.info(msg4)
        self.assertTrue(msg4.splitlines()[-2].strip() == 't')

        self.log.info('''----------------创建同名表-------------------''')
        create_tb3 = f'''drop table if exists s_2.tbone; 
            drop schema if exists s_2;
            create schema s_2;
            create table s_2.tbone(id int, name varchar(20));
            select oid from pg_class where relname='tbone';
            '''
        msg5 = self.commonsh.execut_db_sql(create_tb3)
        self.log.info(msg5)
        oid3 = msg5.splitlines()[-2].strip()
        self.assertTrue(msg5.find('CREATE TABLE') > -1)
        self.log.info('''-------未设置搜索路径直接查询-------''')
        query4 = f'''select pg_table_is_visible({oid3});'''
        msg6 = self.commonsh.execut_db_sql(query4)
        self.log.info(msg6)
        self.assertTrue(msg6.splitlines()[-2].strip() == 'f')
        self.log.info('''-------设置前面搜索路径有同名表-----------''')
        query5 = f'''set search_path to s_1, s_2, public;
            select pg_table_is_visible({oid3});
            '''
        msg7 = self.commonsh.execut_db_sql(query5)
        self.log.info(msg7)
        self.assertTrue(msg7.splitlines()[-2].strip() == 'f')
        self.log.info('''-------设置前面搜索路径没有同名表-----------''')
        query6 = f'''set search_path to s_2, s_1,public;
            select pg_table_is_visible({oid3});
            '''
        msg8 = self.commonsh.execut_db_sql(query6)
        self.log.info(msg8)
        self.assertTrue(msg8.splitlines()[-2].strip() == 't')

    def tearDown(self):
        clear_cmd = f'''drop table if exists s_1.tbone; 
            drop schema if exists s_1;
            drop table if exists s_2.tbone; 
            drop schema if exists s_2;
            '''
        self.commonsh.execut_db_sql(clear_cmd)
        self.log.info('''---
            Opengauss_Function_Innerfunc_Pg_Table_Is_Visible_Case0001结束---''')
