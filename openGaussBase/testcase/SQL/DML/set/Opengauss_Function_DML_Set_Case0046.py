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
--  @date:2020/11/3
--  @testpoint:explain语句，plan参数为on时与其他选项同时使用，合理报错
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0046开始执行-----------------------------')

    def test_explain(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists student;
                                      create table student(id int, name char(20));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
       # explain语句，plan参数与其他参数一起使用，合理报错
       # explain语句，依次按顺序添加参数(省略plan参数)
        sql_cmd2 = commonsh.execut_db_sql('''explain(ANALYZE,VERBOSE,COSTS ,CPU ,BUFFERS,TIMING,plan,format text) insert into student values(1,'a'),(2,'b');
                                       explain(ANALYZE,VERBOSE,COSTS ,CPU ,BUFFERS,TIMING,format text) insert into student values(1,'a'),(2,'b');''')

        logger.info(sql_cmd2)
        self.assertIn("ERROR:  EXPLAIN option 'PLAN' can not work with other options.", sql_cmd2)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd2)
        # explain语句,不按顺序添加参数(省略plan参数)
        # explain语句，不按顺序添加参数(并且添加plan参数)，合理报错
        sql_cmd3 = commonsh.execut_db_sql('''explain(VERBOSE,ANALYZE,COSTS ,CPU,BUFFERS,TIMING,format text) insert into student values(1,'a'),(2,'b');
                                      explain(VERBOSE,ANALYZE,COSTS ,CPU,BUFFERS,TIMING,plan,format text) insert into student values(1,'a'),(2,'b');''')
        logger.info(sql_cmd3)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd3)
        self.assertIn("ERROR:  EXPLAIN option 'PLAN' can not work with other options.", sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd5 = commonsh.execut_db_sql('''drop table student;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0046执行结束--------------------------')
