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
Case Type   : 系统操作
Case Name   : 使用explain不指定ANALYZE选项
Description :
        1.建表
        2.使用explian查询表
        3.使用explain ..insert语句
        4.插入两条数据
        5.使用explain..update语句
        6.explain..delete语句
        7.使用explain..create table as table
        8.删除表
Expect      :
        1.建表成功
        2.显示表简单查询的执行计划
        3.执行成功，实际给表未插入数据
        4.插入两条数据成功
        5.update语句不生效
        6.delete语句不生效
        7.合理报错
        8.删除表成功
History     :
"""
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0043开始执行-----------------------------')

    def test_explain(self):

        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists student;
                                      create table student(id int, name char(20));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''explain select * from student;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql('''explain insert into student values(1,'a'),(2,'b');
                                       select * from student;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd3)
        sql_cmd4 = commonsh.execut_db_sql('''insert into student values(1,'a'),(2,'b');
                                       explain update student set name ='c' where id=1;
                                       explain delete from student;
                                       ''')
        logger.info(sql_cmd4)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd4)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd4)
        sql_cmd5 = commonsh.execut_db_sql('''drop table if exists course cascade;
                                           explain create table course as table student;''')
        logger.info(sql_cmd5)
        self.assertIn('ERROR:  EXPLAIN CREATE TABLE AS SELECT requires ANALYZE', sql_cmd5)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd6 = commonsh.execut_db_sql('''drop table student;''')
        logger.info(sql_cmd6)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0043执行结束--------------------------')
