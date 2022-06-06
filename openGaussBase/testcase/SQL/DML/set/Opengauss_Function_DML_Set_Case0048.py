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
--  @testpoint:使用explain分析带有索引的表查询成功，删除时合理报错
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0048开始执行-----------------------------')

    def test_explain(self):
        # 建表并创建索引
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists student;
                                      create table student(id int, name char(20));
                                      drop index if exists unique_id;
                                      CREATE INDEX unique_id on student(id);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.CREATE_INDEX_SUCCESS_MSG, sql_cmd1)
       # 使用explain分析带有索引的表，显示索引执行信息
       # 使用explain删除索引，合理报错
        sql_cmd2 = commonsh.execut_db_sql('''explain select * from student where id=1;
                                       explain analyze drop index unique_id;''')

        logger.info(sql_cmd2)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd2)
        self.assertIn('ERROR:  syntax error', sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd5 = commonsh.execut_db_sql('''drop table student;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0048执行结束--------------------------')
