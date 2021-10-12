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
--  @testpoint:opengauss关键字nvarchar2(非保留)，自定义数据类型名为nvarchar2
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
         logger.info("------------------------ Opengauss_Function_Keyword_Nvarchar2_Case0035 开始执行--------------------------")

    # 关键字nvarchar2作为数据类型不带引号，创建成功
    def test_text_1(self):
        SqlMdg = commonsh.execut_db_sql('''CREATE TYPE public.nvarchar2 AS (f1 int, f2 text);
                                        select typname from pg_type where typname ='nvarchar2';
                                        drop type public.nvarchar2;''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_TYPE_SUCCESS_MSG, SqlMdg)
        self.assertIn('nvarchar2', SqlMdg)
        self.assertIn(constant.DROP_TYPE_SUCCESS_MSG, SqlMdg)


    # 关键字nvarchar2作为数据类型加双引号，创建成功
    def test_text_2(self):
        SqlMdg = commonsh.execut_db_sql('''CREATE TYPE public."nvarchar2" AS (f1 int, f2 text);
                                        select typname from pg_type where typname ='nvarchar2';
                                        drop type public."nvarchar2";''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_TYPE_SUCCESS_MSG, SqlMdg)
        self.assertIn('nvarchar2',SqlMdg)
        self.assertIn(constant.DROP_TYPE_SUCCESS_MSG, SqlMdg)


    # 关键字nvarchar2作为数据类型加单引号，合理报错
    def test_text_3(self):
        SqlMdg = commonsh.execut_db_sql('''CREATE TYPE public.'nvarchar2' AS (f1 int, f2 text);
                                        select typname from pg_type where typname ='nvarchar2';
                                        drop type public.'nvarchar2';''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)
        self.assertIn('nvarchar2',SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)

    #关键字nvarchar2作为数据类型加反引号，合理报错
    def test_text_4(self):
        SqlMdg = commonsh.execut_db_sql('''CREATE TYPE public.`nvarchar2` AS (f1 int, f2 text);
                                        select typname from pg_type where typname =`nvarchar2`;
                                        drop type public.`nvarchar2`;''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)


    def tearDown(self):
         logger.info('------------------------ Opengauss_Function_Keyword_Nvarchar2_Case0035 执行结束--------------------------')