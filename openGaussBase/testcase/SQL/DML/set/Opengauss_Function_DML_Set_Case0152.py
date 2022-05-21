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
--  @testpoint:在insert语句中，使用explain 语法依次添加BUFFERS,timing,plan选项
'''
import sys
import unittest

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0152开始执行-----------------------------')

    def test_explain(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists student;
                                      create table student(id int, name char(20));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 添加BUFFERS选项，省略false选项(默认行为为false, 是针对analyze的,不是针对buffer的设置)
        # 添加BUFFERS选项，添加false选项,不显示Buffers信息
        # 添加BUFFERS选项，添加true选项，显示Buffers信息
        sql_cmd2 = commonsh.execut_db_sql('''explain (analyze,buffers)insert into student values(5,'a'),(6,'b');
                                      explain (analyze,buffers false)insert into student values(5,'a'),(6,'b');
                                      explain (analyze,buffers true)insert into student values(5,'a'),(6,'b');''')
        logger.info(sql_cmd2)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd2)
        # 添加timing选项，省略true选项，显示actual time
        # 添加timing选项，添加true选项，显示actual time
        # 添加timing选项，添加false选项(不显示启动时间和花费在输出节点上的时间信息)
        sql_cmd3 = commonsh.execut_db_sql('''explain (analyze,timing)insert into student values(5,'a'),(6,'b');
                                      explain (analyze,timing true)insert into student values(5,'a'),(6,'b');
                                      explain (analyze,timing false)insert into student values(5,'a'),(6,'b');''')
        logger.info(sql_cmd3)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd3)
        # 添加plan选项，省略on选项，返回EXPLAIN SUCCESS;查询plan_table表信息，数据增加到plan_table表
        # 添加plan选项，添加on选项，返回EXPLAIN SUCCESS;查询plan_table表信息，数据增加到plan_table表
        # 添加plan选项，添加off选项，不存储执行计划，将执行计划打印到当前屏幕
        sql_cmd4 = commonsh.execut_db_sql('''explain (plan)insert into student values(5,'a'),(6,'b');
                                       select * from plan_table;
                                       explain (plan on)insert into student values(5,'a'),(6,'b');
                                       select * from plan_table;
                                       explain (plan off)insert into student values(5,'a'),(6,'b');''')
        logger.info(sql_cmd4)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd4)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd4)
    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd5 = commonsh.execut_db_sql('''drop table student;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0152执行结束--------------------------')
