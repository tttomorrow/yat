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
Case Name： octet_length校验入参
Descption:octet_length(string)二进制字符串中的字节数。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.octet_length入参异常校验报错
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
        logger.info("------------------------Opengauss_Function_Binarystring_Octet_Length_Case0002开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_octet_length(self):

        logger.info("-----------非bytea-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT octet_length('hABCDEFGHIJK'::RAW);""")
        logger.info(Normal_SqlMdg2)
        self.assertIn('ERROR:  invalid hexadecimal digit: "h"', Normal_SqlMdg2)
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT octet_length(E'jo\\\\\\00\\"0se'::bytea) AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertIn('ERROR:  invalid input syntax for type bytea', Normal_SqlMdg3)

        logger.info("-----------多参、少参、空值-----------")
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT octet_length('young man','young man');""")
        logger.info(Normal_SqlMdg4)
        self.assertIn('does not exist', Normal_SqlMdg4)
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT octet_length();""")
        logger.info(Normal_SqlMdg5)
        self.assertIn('does not exist', Normal_SqlMdg5)
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""SELECT octet_length('');""")
        logger.info(Normal_SqlMdg6)
        self.assertTrue(Normal_SqlMdg6.splitlines()[2].count(' ') == 13)

    def tearDown(self):

        logger.info('------------------------Opengauss_Function_Binarystring_Octet_Length_Case0002执行结束--------------------------')