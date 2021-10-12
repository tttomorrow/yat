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
Case Type   : analyze--临时表
Case Name   : 存储过程中使用ANALYZE临时表
Description :
    1.创建表并插入数据
    2.创建存储过程中使用analyze语句
    3.创建存储过程中使用analyze verbose语句
    4.删除存储过程
    5.删除表
Expect      :
    1.建表成功且数据插入成功
    2.存储过程创建成功
    3.存储过程创建成功
    4.存储过程删除成功
    5.表删除成功
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


class SYSOPERATION(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0135开始执行-----------------------------')

    def test_analyze(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists test;
       create table  test(id  int,name varchar(100),ctime date);
       insert into test values (1,'test','2018-09-17 16:10:28');''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''create temporary table LSB_abc as select * from test;
       select * from LSB_abc; ''')
        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql('''
       create or replace procedure p1(str boolean) is
       begin
       analyze LSB_abc;
       end;
       create or replace procedure p1(str boolean) is
       begin
       analyze verbose LSB_abc;
       end;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.CREATE_PROCEDURE_SUCCESS_MSG, sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''drop procedure p1;
        drop table test;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0135执行结束--------------------------')
