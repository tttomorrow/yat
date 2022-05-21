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
--  @testpoint:在insert语句中，使用explain 语法依次添加语法中的参数
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0044开始执行-----------------------------')

    def test_explain(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists student;
                                      create table student(id int, name char(20));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # explain添加analyze参数，省略true选项，显示实际运行时间和其他统计数据
        # explain添加analyze参数，添加true选项，显示实际运行时间和其他统计数据
        sql_cmd2 = commonsh.execut_db_sql('''explain analyze insert into student values(1,'a'),(2,'b');
                                       explain (analyze true) insert into student values(1,'a'),(2,'b'); ''')
        logger.info(sql_cmd2)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd2)
        # explain添加analyse参数，省略true选项，显示实际运行时间和其他统计数据
        # explain添加analyse参数，添加true选项，显示实际运行时间和其他统计数据
        sql_cmd3 = commonsh.execut_db_sql('''explain analyse insert into student values(1,'a'),(2,'b');
                                       explain (analyse true) insert into student values(1,'a'),(2,'b');''')
        logger.info(sql_cmd3)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd3)
        # explain添加analyze参数，添加false选项，不显示实际运行时间
        # explain添加analyse参数，添加false选项，不显示实际运行时间
        sql_cmd4 = commonsh.execut_db_sql('''explain (analyze false) insert into student values(1,'a'),(2,'b');
                                       explain (analyse false) insert into student values(1,'a'),(2,'b');''')
        logger.info(sql_cmd4)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd4)
        # explain添加verbose参数，省略true选项，显示有关计划的额外信息
        # explain添加verbose参数，添加true选项，显示有关计划的额外信息
        # explain添加verbose参数，添加false选项，不显示有关计划的Output额外信息
        sql_cmd5 = commonsh.execut_db_sql('''explain verbose insert into student values(3,'a'),(4,'b');
                                       explain (verbose true) insert into student values(3,'a'),(4,'b');
                                       explain (verbose false) insert into student values(3,'a'),(4,'b');''')
        logger.info(sql_cmd5)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd5)
        # explain添加costs参数，省略true选项，显示估计总成本和宽度
        # explain添加costs参数，添加true选项，显示估计总成本和宽度
        # explain添加costs参数，添加false选项，不显示估计总成本和宽度
        sql_cmd6 = commonsh.execut_db_sql('''explain (COSTS)insert into student values(5,'a'),(6,'b');
                                      explain (COSTS true)insert into student values(5,'a'),(6,'b');
                                      explain (COSTS false)insert into student values(5,'a'),(6,'b');''')
        logger.info(sql_cmd6)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd6)
        # explain添加cpu参数，省略true选项，显示CPU的使用情况
        # explain添加cpu参数，添加true选项，显示CPU的使用情况
        # explain添加cpu参数，添加false选项，不显示CPU的使用情况
        sql_cmd7 = commonsh.execut_db_sql('''explain (analyze,cpu)insert into student values(5,'a'),(6,'b');
                                      explain (analyze,cpu true)insert into student values(5,'a'),(6,'b');
                                      explain (analyze,cpu false)insert into student values(5,'a'),(6,'b');''')
        logger.info(sql_cmd7)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd7)
    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd8 = commonsh.execut_db_sql('''drop table student;''')
        logger.info(sql_cmd8)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0044执行结束--------------------------')
