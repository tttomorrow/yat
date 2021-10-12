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
Case Name   : 建表添加参数on commit preserve rows,退出会话，表数据不存在
Description :
    1.创建临时表，添加参数on commit preserve rows
    2.插入数据
    3.查询表数据
    4.退出会话，查询表数据
    5.删表
Expect      :
    1.建表成功
    2.数据插入成功
    3.表有数据
    4.查询表无数据
    5.删表成功
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Temporarytable(unittest.TestCase):
    def setup(self):
        logger.info('------------------------Opengauss_Function_DDL_Temporarytable_Case0017开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_temporary_table(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists temp_table_alter_017;
       create global TEMPORARY table temp_table_alter_017(
       c_id int,
       c_real real,
       c_char char(50) default null,
       c_clob clob,
       c_raw raw(20),
       c_blob blob,
       c_date date
       )on commit preserve rows;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''
        insert into temp_table_alter_017 select * from temp_table_alter_017;
        insert into temp_table_alter_017 select * from temp_table_alter_017;
        select count(*) from temp_table_alter_017;
        \\q''')
        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
        self.assertIn('8', sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql('''select count(*) from temp_table_alter_017;''')
        logger.info(sql_cmd3)
        self.assertIn('0', sql_cmd3)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''drop table if exists temp_table_alter_017;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DDL_Temporarytable_Case0017执行结束--------------------------')
