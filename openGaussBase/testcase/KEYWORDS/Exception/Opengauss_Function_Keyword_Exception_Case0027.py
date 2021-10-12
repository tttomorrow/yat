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
--  @date:2020/8/14
--  @testpoint:opengauss关键字exception非保留)，作为序列名
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
        logger.info("------------------------Opengauss_Function_KeyWord_exception_Case0027开始执行--------------------------")

    # 关键字不带引号 - 成功
    def test_do_1(self):
        logger.info("------------------------关键字不带引号 - 成功--------------------------")
        SqlMdg = commonsh.execut_db_sql(''' create sequence exception start 100 cache 50;
                                            drop sequence public.exception;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_SEQUENCE_SUCCESS_MSG, SqlMdg)
        self.assertIn(constant.CREATE_SEQUENCE_SUCCESS_MSG, SqlMdg)
        self.assertIn(constant.DROP_SEQUENCE_SUCCESS_MSG, SqlMdg)



    # 关键字带双引号-成功
    def test_do_2(self):
        logger.info("------------------------关键字带双引号-成功--------------------------")
        SqlMdg = commonsh.execut_db_sql('''create sequence public."exception" start 100 cache 50;
                                        drop sequence public."exception";''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_SEQUENCE_SUCCESS_MSG, SqlMdg)
        self.assertIn(constant.CREATE_SEQUENCE_SUCCESS_MSG, SqlMdg)
        self.assertIn(constant.DROP_SEQUENCE_SUCCESS_MSG, SqlMdg)

    # 关键字带单引号-合理报错
    def test_do_3(self):
        logger.info("------------------------关键字带单引号-合理报错--------------------------")
        SqlMdg = commonsh.execut_db_sql('''drop sequence if exists public.'exception';
                                        create sequence public.'exception' start 100 cache 50;''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)



    #关键字带反引号-合理报错
    def test_do_4(self):
        logger.info("------------------------关键字带反引号-合理报错--------------------------")
        SqlMdg = commonsh.execut_db_sql('''drop sequence if exists public.`exception`;
                                        create sequence public.`exception` start 100 cache 50;''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)

    def tearDown(self):
        logger.info('------------------------Opengauss_Function_KeyWord_exception_Case0027执行结束--------------------------')