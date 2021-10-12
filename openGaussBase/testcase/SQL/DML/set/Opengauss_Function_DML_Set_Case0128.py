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
--  @testpoint:设置模式搜索路径
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0128开始执行-----------------------------')

    def test_reset(self):
        # 将搜索路径设置为myschema、public，首先搜索myschema
        sql_cmd1 = commonsh.execut_db_sql('''SHOW SEARCH_PATH;
                                       drop schema if exists myschema cascade;
                                       create schema myschema;
                                       SET SEARCH_PATH TO myschema, public;
                                       drop table if exists my_table;
                                       create table my_table(id int);''')
        logger.info(sql_cmd1)
        self.assertIn('"$user",public', sql_cmd1)
        self.assertIn(constant.CREATE_SCHEMA_SUCCESS_MSG, sql_cmd1)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 恢复搜索路径默认值
        sql_cmd2 = commonsh.execut_db_sql('''reset SEARCH_PATH;
        SHOW SEARCH_PATH;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.RESET_SUCCESS_MSG, sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表和模式
        sql_cmd3 = commonsh.execut_db_sql('''drop schema myschema cascade;
        drop table my_table;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0128执行结束--------------------------')
