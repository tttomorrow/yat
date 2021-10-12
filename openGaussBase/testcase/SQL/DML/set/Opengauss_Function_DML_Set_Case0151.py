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
Case Type   : 系统操作-explain
Description :
        1.建表
        2.explain添加detail参数
        3.explain添加nodes选项
        4.添加nodes_num选项
        5.删表
Expect      :
        1.建表成功
        2.执行成功
        3.合理报错
        4.合理报错
        5.删表成功
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0151开始执行-----------------------------')
        self.Constant = Constant()
    def test_explain(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists student;
                                      create table student(id int, name char(20));''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # explain添加detail参数，省略true选项
        # explain添加detail参数，添加true选项
        # explain添加detail参数，添加false选项
        sql_cmd2 = commonsh.execut_db_sql('''explain (analyze,detail)insert into student values(5,'a'),(6,'b');
                                      explain (analyze,detail true)insert into student values(5,'a'),(6,'b');
                                      explain (analyze,detail false)insert into student values(5,'a'),(6,'b');''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.EXPLAIN_SUCCESS_MSG, sql_cmd2)
        # explain添加nodes选项，省略true选项
        # explain添加nodes选项，添加true选项
        # explain添加nodes选项，添加false选项
        sql_cmd3 = commonsh.execut_db_sql('''explain (analyze,nodes)insert into student values(5,'a'),(6,'b');
                                       explain (analyze,nodes true)insert into student values(5,'a'),(6,'b');
                                       explain (analyze,nodes false)insert into student values(5,'a'),(6,'b');''')
        logger.info(sql_cmd3)
        self.assertIn('ERROR:  unrecognized EXPLAIN option "nodes"', sql_cmd3)
        # 添加nodes_num选项，省略true选项
        # 添加nodes_num选项，添加true选项
        # 添加nodes_num选项，添加false选项
        sql_cmd4 = commonsh.execut_db_sql('''explain (analyze,num_nodes)insert into student values(5,'a'),(6,'b');
                                       explain (analyze,num_nodes true)insert into student values(5,'a'),(6,'b');
                                       explain (analyze,num_nodes false)insert into student values(5,'a'),(6,'b');''')
        logger.info(sql_cmd4)
        self.assertIn('ERROR:  unrecognized EXPLAIN option "num_nodes"', sql_cmd4)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd5 = commonsh.execut_db_sql('''drop table student;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0151执行结束--------------------------')
