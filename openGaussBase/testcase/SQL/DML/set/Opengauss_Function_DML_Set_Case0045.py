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
--  @testpoint:在insert语句中，使用explain语法，添加format参数测试
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0045开始执行-----------------------------')

    def test_explain(self):
        # 建表并插入一条数据
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists student;
                                      create table student(id int, name char(20));
                                      explain analyze insert into student values(5,'a'),(6,'b');''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd1)
       # 查看explain_perf_mode参数值（pretty）
       # 使用format参数，指定输出格式为text
       # 修改explain_perf_mode为normal并查看
       # 以JSON格式输出的执行计划
       # 以YAML格式输出的执行计划;以YAML格式输出的执行计划，添加where条件
       # 以xml格式输出的执行计划;以xml格式输出的执行计划，添加where条件
       # 以csv格式输出执行计划，合理报错
       # 以ymal1格式输出执行计划，合理报错
        sql_cmd2 = commonsh.execut_db_sql('''show explain_perf_mode;
                                      explain (format text)select * from student;
                                      SET explain_perf_mode=normal;
                                      show explain_perf_mode;
                                      explain (format json)select * from student;
                                      explain (format yaml)select * from student;
                                      explain (format yaml)select * from student where id =1;
                                      explain (format xml)select * from student;
                                      explain (format xml)select * from student where id=1;
                                      explain (format csv)select * from student;
                                      explain (format yaml1)select * from student; ''')
        logger.info(sql_cmd2)
        self.assertIn('pretty', sql_cmd2)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd2)
        self.assertIn('normal', sql_cmd2)
        self.assertIn('ERROR:  unrecognized value for EXPLAIN option "format": "csv"', sql_cmd2)
        self.assertIn('ERROR:  unrecognized value for EXPLAIN option "format": "yaml1"', sql_cmd2)
        # 修改explain_perf_mode值为run;以ymal格式输出执行计划，合理报错
        sql_cmd3 = commonsh.execut_db_sql('''set explain_perf_mode=run;
                                      explain (format yaml) select * from student;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd3)
        self.assertIn('ERROR:  explain_perf_mode requires FORMAT TEXT', sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd5 = commonsh.execut_db_sql('''drop table student;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0045执行结束--------------------------')
