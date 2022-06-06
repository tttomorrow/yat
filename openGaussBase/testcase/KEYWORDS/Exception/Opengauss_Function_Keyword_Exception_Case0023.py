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
--  @testpoint:opengauss关键字exception非保留)，作为索引名

'''

import unittest

from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Hostname(unittest.TestCase):

    def setUp(self):
         logger.info("------------------------ Opengauss_Function_Keyword_Exception_Case0023 开始执行--------------------------")

    # 前置条件，创建一个表
    def test_az_1(self):
        SqlMdg = commonsh.execut_db_sql('''drop table if exists explain_test;
                                        create table explain_test(id int,name varchar(10));''')
        logger.info(SqlMdg)
        self.assertIn(constant.TABLE_DROP_SUCCESS, SqlMdg)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, SqlMdg)

    # 关键字不带引号 - 成功
    def test_do_1(self):
        SqlMdg = commonsh.execut_db_sql('''create index public.exception on explain_test(id);
                                        drop index public.exception;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_INDEX_SUCCESS_MSG, SqlMdg)
        self.assertIn(constant.CREATE_INDEX_SUCCESS_MSG, SqlMdg)
        self.assertIn(constant.DROP_INDEX_SUCCESS_MSG, SqlMdg)

    # 关键字带双引号-成功
    def test_do_2(self):
        SqlMdg = commonsh.execut_db_sql('''create index public."exception" on explain_test(id);
                                        drop index public."exception";''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_INDEX_SUCCESS_MSG, SqlMdg)
        self.assertIn(constant.CREATE_INDEX_SUCCESS_MSG, SqlMdg)
        self.assertIn(constant.DROP_INDEX_SUCCESS_MSG, SqlMdg)

    # 关键字带单引号-合理报错
    def test_do_3(self):
        SqlMdg = commonsh.execut_db_sql('''create index public.'exception' on explain_test(id);''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)

    # 关键字带反引号-合理报错
    def test_do_4(self):
        SqlMdg = commonsh.execut_db_sql('''create index public.`exception` on explain_test(id);''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)

    def tearDown(self):
         logger.info('------------------------ Opengauss_Function_Keyword_Exception_Case0023 执行结束--------------------------')