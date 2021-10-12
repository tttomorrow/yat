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
Case Type   : 系统操作
Case Name   : 事务中使用EXPLAIN ANALYZE 语句
Description :
        1.建表
        2.开启事务
        3.事务中使用explain语句
        4.回滚
        5.查询表
        6.事务中，使用explain..craete table ..as
        7.回滚
        8.查询course表
        9.删表
Expect      :
        1.建表成功
        2.开启事务成功
        3.插入，更新，删除成功
        4.回滚成功
        5.表数据回到执行explain语句前，数据为空
        6.建表成功
        7.回滚成功
        8.course表不存在
        9.删表成功
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0050开始执行-----------------------------')

    def test_explain(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists student;
                                      create table student(id int, name char(20));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''start transaction;
                                      explain analyze insert into student values(1,'lilu');
                                      explain analyze update student set name='kili' where id=1;
                                      explain analyze delete from student;
                                      rollback;
                                      select * from student;''')

        logger.info(sql_cmd2)
        self.assertIn(constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.ROLLBACK_MSG, sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql('''start transaction;
                                          drop table if exists course cascade;
                                          explain analyze create table course as table student;
                                          select * from course;
                                          rollback;
                                          select * from course;''')

        logger.info(sql_cmd3)
        self.assertIn(constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd3)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd3)
        self.assertIn(constant.ROLLBACK_MSG, sql_cmd3)
        self.assertIn('relation "course" does not exist', sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''drop table student;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0050执行结束--------------------------')
