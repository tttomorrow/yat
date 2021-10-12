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
Case Type   : 临时表
Case Name   : 创建和普通表重名的临时表
Description :
    1.创建普通表
    2.查询表信息
    3.创建和普通表同名的临时表
    4.查询表信息
    5.删表
Expect      :
    1.建表成功
    2.模式为public
    3.建表成功
    4.模式为pg_temp开头的模式
    5.删表成功（先删除的是临时表）
History     :
"""
import sys
import unittest

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Temporarytable(unittest.TestCase):
    def setup(self):
        logger.info(
            '------------------------Opengauss_Function_DDL_Temporarytable_Case0036开始执行-----------------------------')

    def test_temporary_table(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists temp_table_036;
        create table temp_table_036(a int);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql(
            '''select schemaname,tablename from pg_tables where tablename = 'temp_table_036';''')
        logger.info(sql_cmd2)
        self.assertIn('public', sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql('''create temporary table temp_table_036(a int);
        select schemaname,tablename from pg_tables where tablename = 'temp_table_036';''')
        logger.info(sql_cmd3)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd3)
        self.assertIn('pg_temp', sql_cmd3)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd5 = commonsh.execut_db_sql('''drop table if exists temp_table_036;
       drop table if exists temp_table_036;''')
        logger.info(sql_cmd5)
        logger.info(
            '------------------------Opengauss_Function_DDL_Temporarytable_Case0036执行结束--------------------------')
