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
'''
--  @date:2020/10/30
--  @testpoint:创建复合类型，复合类型的列的现有数据类型为二进制类型
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

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0004开始执行-----------------------------')

    def test_common_user_permission(self):
        # 创建一种复合类型
        sql_cmd1 = commonsh.execut_db_sql('''drop type if exists t_type4 cascade;
                                      CREATE TYPE t_type4 AS (f1 BLOB, f2 RAW,f3 BYTEA);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_TYPE_SUCCESS_MSG, sql_cmd1)
        # 建表1
        sql_cmd2 = commonsh.execut_db_sql('''drop table if exists t1_test;
                                       CREATE TABLE t1_test(a int, b t_type4);''')
        logger.info(sql_cmd2)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd2)
        # 建表2
        sql_cmd3 = commonsh.execut_db_sql('''drop table if exists t2_test;
                                      CREATE TABLE t2_test(a int, b t_type4);''')
        logger.info(sql_cmd3)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd3)
        # 表1插入数据
        sql_cmd4 = commonsh.execut_db_sql('''INSERT INTO t1_test values(1,(empty_blob(),HEXTORAW('DEADBEEF'),E'\\\\\\xDEADBEEF'));''')
        logger.info(sql_cmd4)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd4)
        # 表2插入数据
        sql_cmd5 = commonsh.execut_db_sql('''INSERT INTO t2_test select * from t1_test;''')
        logger.info(sql_cmd5)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd5)
        # 查询表1b字段的所有值
        sql_cmd6 = commonsh.execut_db_sql('''select (b).f1, (b).f2 ,(b).f3 from t1_test;''')
        logger.info(sql_cmd6)
        self.assertIn('DEADBEEF', sql_cmd6)
        # 表1和表2联合查询
        sql_cmd7 = commonsh.execut_db_sql('''SELECT * FROM t1_test t1 join t2_test t2 on (t1.b).f1=(t2.b).f1;''')
        logger.info(sql_cmd7)
        self.assertIn('DEADBEEF', sql_cmd7)
    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd8 = commonsh.execut_db_sql('''drop table t1_test;
                                   drop table t2_test;''')
        logger.info(sql_cmd8)
        # 删除类型
        sql_cmd9 = commonsh.execut_db_sql('''drop type t_type4 cascade;''')
        logger.info(sql_cmd9)
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0004执行结束--------------------------')





