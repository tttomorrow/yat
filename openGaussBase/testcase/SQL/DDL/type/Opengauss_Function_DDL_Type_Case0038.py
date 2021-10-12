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
--  @date:2020/10/30
--  @testpoint:修改类型名称,名称有模式修饰
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

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0038开始执行-----------------------------')

    def test_common_user_permission(self):
        # 创建模式
        sql_cmd1 = commonsh.execut_db_sql('''drop schema if exists test_schema2 cascade;
                                       create schema test_schema2;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_SCHEMA_SUCCESS_MSG, sql_cmd1)
        # 创建枚举类型
        sql_cmd2 = commonsh.execut_db_sql('''drop type if exists test_schema2.bugstatus3 cascade;
                                      CREATE TYPE test_schema2.bugstatus3 AS ENUM ('create', 'modify', 'closed');''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_TYPE_SUCCESS_MSG, sql_cmd2)
        # 修改类型名称
        sql_cmd3 = commonsh.execut_db_sql('''ALTER TYPE test_schema2.bugstatus3 RENAME TO bugstatus3_new;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.ALTER_TYPE_SUCCESS_MSG, sql_cmd3)
        # 查看类型信息
        sql_cmd4 = commonsh.execut_db_sql('''\\dT+ test_schema2.bugstatus3_new''')
        logger.info(sql_cmd4)
        self.assertIn('test_schema2.bugstatus3_new', sql_cmd4)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除类型
        sql_cmd5 = commonsh.execut_db_sql('''drop type test_schema2.bugstatus3_new cascade;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0038执行结束--------------------------')





