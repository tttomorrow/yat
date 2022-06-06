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
"""
Case Type   : 功能测试
Case Name   : quote_literal处理带转义字符的二进制
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.入参为转义字符\n,\f等
Expect      :
    步骤 1：数据库状态正常
    步骤 2：函数返回结果正确
History     :
"""

import unittest
from yat.test import macro
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Bit_string_function(unittest.TestCase):

    def setUp(self):
        logger.info("----------- Opengauss_Function_Innerfunc_Quote_Literal_Case0005 开始执行--------------")
        self.commonsh = CommonSH('dbuser')

    def test_quote_literal(self):
        logger.info("-----------返回适用于SQL语句的标识符形式-----------")

        sql_cmd1 = '''SELECT quote_literal(E'O\\'hello');'''
        msg1 = self.commonsh.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertTrue(msg1.splitlines()[2].strip().strip("'") == 'O\'\'hello')

        sql_cmd2 = '''SELECT quote_literal(E'O\\nhello');'''
        msg2 = self.commonsh.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertTrue(msg2.splitlines()[2].strip().strip("'") == 'O           +')
        self.assertTrue(msg2.splitlines()[3].strip().strip("'") == 'hello')

        sql_cmd3 = '''SELECT quote_literal(E'O\thello');'''
        msg3 = self.commonsh.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        self.assertTrue(msg3.splitlines()[2].strip().strip("'") == 'O      hello')

        sql_cmd4 = '''SELECT quote_literal(E'O\\hello');'''
        msg4 = self.commonsh.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        self.assertTrue(msg4.splitlines()[2].strip().strip("'") == 'Ohello')

        sql_cmd5 = '''SELECT quote_literal(E'O\\\\\fhello');'''
        msg5 = self.commonsh.execut_db_sql(sql_cmd5)
        logger.info(msg5)
        self.assertTrue(msg5.splitlines()[2].strip().strip("'") == 'O\\x0Chello')

    def tearDown(self):
        logger.info('-------------Opengauss_Function_Innerfunc_Quote_Literal_Case0005执行结束-------------')
