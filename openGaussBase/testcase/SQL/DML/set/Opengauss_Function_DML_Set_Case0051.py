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
--  @testpoint:显示SQL语句的执行计划，且要按顺序给出选项
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0051开始执行-----------------------------')

    def test_explain(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists student;
                                      create table student(id int, name char(20));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # explain语句，依次按analyze/analyse添加verbose参数
        sql_cmd2 = commonsh.execut_db_sql('''explain analyze verbose insert into student values(1,'a');
                                      explain analyse verbose insert into student values(1,'a');
                                      explain PERFORMANCE insert into student values(1,'a');''')

        logger.info(sql_cmd2)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd2)
        # explain语句，依次添加参数verbose，analyze/analyse，合理报错
        # explain不按顺序添加PERFORMANCE语句，合理报错
        sql_cmd3 = commonsh.execut_db_sql('''explain verbose analyze insert into student values(1,'a');
                                      explain verbose analyse insert into student values(1,'a');
                                      PERFORMANCE explain insert into student values(1,'a');''')

        logger.info(sql_cmd3)
        self.assertIn('ERROR:  syntax error', sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd3 = commonsh.execut_db_sql('''drop table student;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0051执行结束--------------------------')
