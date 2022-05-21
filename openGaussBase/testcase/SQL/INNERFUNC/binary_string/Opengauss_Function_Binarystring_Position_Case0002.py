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

Case Type： 功能测试
Case Name： position入参异常报错校验
Descption:position(substring in string)特定子字符串的位置。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.position的入参异常进行报错校验
'''
import os
import unittest
from yat.test import Node
from yat.test import macro
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH

logger = Logger()

class Bit_string_function(unittest.TestCase):

    def setUp(self):
        logger.info("------------------------Opengauss_Function_Binarystring_Position_Case0002开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_position(self):

        logger.info("-----------len(s1)>len(s2)，不存在返回''-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT position(E'\\\\\\000omassss'::bytea in E'Th\\\\\\000omas'::bytea) AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[2].strip(' ') == '0')

        logger.info("-----------入参错误-----------")
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT position(E'\\\\\\xabcdef'::bytea in E'\\\\\\x98765abcdef3210'::bytea);""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue('ERROR:  invalid hexadecimal data: odd number of digits' in Normal_SqlMdg4)

        logger.info("-----------缺少关键字-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT position(E'\\\\\\xabcdef'::bytea , E'\\\\\\x98765abc9def3210'::bytea);""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue('ERROR:  syntax error' in Normal_SqlMdg5)

        logger.info("-----------多参、少参、空值-----------")
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""SELECT position(E'\\\\\\000om'::bytea in E'Th\\\\\\000omas'::bytea, E'Th\\\\\\000omas'::bytea) AS RESULT;""")
        logger.info(Normal_SqlMdg6)
        self.assertTrue('ERROR:  syntax error' in Normal_SqlMdg6)
        Normal_SqlMdg7 = self.commonsh.execut_db_sql("""SELECT position(E'\\\\\\000om'::bytea in ) AS RESULT;""")
        logger.info(Normal_SqlMdg7)
        self.assertTrue('ERROR:  syntax error' in Normal_SqlMdg7)
        Normal_SqlMdg8 = self.commonsh.execut_db_sql("""SELECT position(E''::bytea in E'Th\\\\\\000omas'::bytea) AS RESULT;""")
        logger.info(Normal_SqlMdg8)
        self.assertTrue(Normal_SqlMdg8.splitlines()[2].strip(' ') == '')
        Normal_SqlMdg9 = self.commonsh.execut_db_sql("""SELECT position(E'\\\\\\000om'::bytea in E''::bytea) AS RESULT;""")
        logger.info(Normal_SqlMdg9)
        self.assertTrue(Normal_SqlMdg9.splitlines()[2].strip(' ') == '')

    def tearDown(self):

        logger.info('------------------------Opengauss_Function_Binarystring_Position_Case0002执行结束--------------------------')