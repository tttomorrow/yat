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
Case Name： get_byte入参异常
Descption:get_byte(string, offset)从字符串中抽取字节。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.get_byte入参为异常验证报错
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
        logger.info("------------------------Opengauss_Function_Binarystring_Get_Byte_Case0002开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_get_byte(self):

        logger.info("-----------超过索引-----------")
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("""SELECT get_byte('young man',11);""")
        logger.info(Normal_SqlMdg1)
        self.assertIn('out of valid range', Normal_SqlMdg1)

        logger.info("-----------非bytea-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT get_byte(right('*&^%$%&^*', 100),7);""")
        logger.info(Normal_SqlMdg2)
        self.assertIn('does not exist', Normal_SqlMdg2)
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT get_byte(rawcat(left('ABCDEFGHIJK', 6)::RAW,'0123456789'::RAW)::bytea,15);""")
        logger.info(Normal_SqlMdg3)
        self.assertIn('cannot cast type raw to bytea', Normal_SqlMdg3)

        logger.info("-----------多参、少参、空值-----------")
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT get_byte('young man',4，5);""")
        logger.info(Normal_SqlMdg4)
        self.assertIn('ERROR:  syntax error', Normal_SqlMdg4)
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT get_byte('young man');""")
        logger.info(Normal_SqlMdg5)
        self.assertIn('does not exist', Normal_SqlMdg5)
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""SELECT get_byte(4);""")
        logger.info(Normal_SqlMdg6)
        self.assertIn('does not exist', Normal_SqlMdg6)
        Normal_SqlMdg7 = self.commonsh.execut_db_sql("""SELECT get_byte('',5);""")
        logger.info(Normal_SqlMdg7)
        logger.info(len(Normal_SqlMdg7.splitlines()[2]))
        self.assertTrue(Normal_SqlMdg7.splitlines()[2] == '         ')
    def tearDown(self):
        logger.info('------------------------Opengauss_Function_Binarystring_Get_Byte_Case0002执行结束--------------------------')