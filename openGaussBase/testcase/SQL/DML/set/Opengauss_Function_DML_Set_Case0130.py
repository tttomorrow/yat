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
--  @date:2020/11/10
--  @testpoint:使用explain语句，分析多个表
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0130开始执行-----------------------------')

    def test_explain(self):
        # 使用explain分析两个系统表
        sql_cmd1 = commonsh.execut_db_sql('''explain SELECT a.usename,b.locktime FROM pg_user a,pg_user_status b WHERE a.usesysid=b.roloid;
        explain SELECT a.usename,b.locktime,a.usesuper FROM pg_user a FULL JOIN pg_user_status b on a.usesysid=b.roloid;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd1)
        # 建表并插入数据
        sql_cmd2 = commonsh.execut_db_sql('''drop table if exists my_table;
       create table my_table (id int,name varchar(20));
       insert into my_table values(1,'Wiliian'),(2,'Nakli'),(3,'uisvc'),(4,'yuiy');''')
        logger.info(sql_cmd2)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
        # explain,结合union语句，分析一个表
        sql_cmd3 = commonsh.execut_db_sql('''explain select id,name from my_table where name like 'W%' union select id,name from my_table where name like 'N%';''')
        logger.info(sql_cmd3)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd3)
    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''drop table my_table;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0130执行结束--------------------------')
