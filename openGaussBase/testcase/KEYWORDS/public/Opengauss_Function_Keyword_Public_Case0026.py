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
--  @date:2020/9/27
--  @testpoint:opengauss关键字public(非保留)，作为模式名
'''


import unittest
from yat.test import Node

from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Hostname(unittest.TestCase):


    def setUp(self):
        logger.info("------------------------Opengauss_Function_KeyWord_Public_Case0026开始执行--------------------------")
        self.userNode = Node('dbuser')

    def test_do_1(self):
        logger.info("------------------------关键字不带引号 - 成功--------------------------")
        SqlMdg = commonsh.execut_db_sql('''drop schema if exists public cascade;
                                        create schema public;
                                        drop schema if exists public cascade;''')
        logger.info(SqlMdg)
        self.assertIn('DROP SCHEMA', SqlMdg)
        self.assertIn('CREATE SCHEMA', SqlMdg)
        self.assertIn('DROP SCHEMA', SqlMdg)

        logger.info("------------------------关键字带双引号-成功--------------------------")
        SqlMdg = commonsh.execut_db_sql('''drop schema if exists "public" cascade;
                                         create schema "public";
                                         drop schema if exists "public" cascade;''')
        logger.info(SqlMdg)
        self.assertIn('DROP SCHEMA', SqlMdg)
        self.assertIn('CREATE SCHEMA', SqlMdg)
        self.assertIn('DROP SCHEMA', SqlMdg)

        logger.info("------------------------关键字带单引号-合理报错--------------------------")
        SqlMdg = commonsh.execut_db_sql('''create sequence public.'date' start 100 cache 50;''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)

        logger.info("------------------------关键字带反引号-合理报错--------------------------")
        SqlMdg = commonsh.execut_db_sql('''create sequence public.`date` start 100 cache 50;''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)


    def tearDown(self):
        logger.info('------------------------恢复环境--------------------------')

        db_name = self.userNode.db_user
        SqlMdg = commonsh.execut_db_sql(f'''create schema public;
                                        GRANT ALL ON SCHEMA public TO {db_name};
                                        GRANT USAGE  ON SCHEMA public TO public;''')
        logger.info(SqlMdg)
        self.assertIn('CREATE SCHEMA', SqlMdg)
        logger.info("------------------------Opengauss_Function_KeyWord_Public_Case0026执行结束--------------------------")