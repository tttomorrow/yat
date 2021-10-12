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
Case Type   : 常量与宏
Case Name   : CURRENT_SCHEMA有效值测试
Description :
    1.查看默认模式
    2.创建新模式
    3.切换新模式
    4.查看current_schema
    5.删除模式
Expect      :
    1.显示public
    2.创建新模式成功
    3.切换新模式成功
    4.显示myschema
    5.模式删除成功
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Constants_Macros(unittest.TestCase):
    def setUp(self):
        logger.info(
            '------------------------Opengauss_Function_DDL_Constants_Macros_Case0005开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_current_schema(self):
        sql_cmd1 = commonsh.execut_db_sql('''select current_schema;
                                           drop schema if exists myschema cascade;
                                           create schema myschema;''')
        logger.info(sql_cmd1)
        self.res = sql_cmd1.splitlines()[-2].strip()
        self.assertIn(constant.CREATE_SCHEMA_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''SET SEARCH_PATH TO myschema;
                                          select current_schema;
                                          select current_schema();''')
        logger.info(sql_cmd2)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd2)
        self.assertIn('myschema', sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''drop schema myschema cascade;''')
        logger.info(sql_cmd3)
        logger.info(
            '------------------------Opengauss_Function_DDL_Constants_Macros_Case0005执行结束--------------------------')
