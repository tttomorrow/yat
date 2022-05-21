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
Case Name： get_bit操作二进制字符串
Descption:get_bit(string, offset)从字符串中抽取位。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.get_bit入参为二进制字符串
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
        logger.info("------------------------Opengauss_Function_Binarystring_Get_Bit_Case0001开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'escape';''')
        logger.info(SqlMdg1)

    def test_getbit(self):

        logger.info("-----------二进制字符串-----------")
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT get_bit(E'a'::bytea, 0) = 1 AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == 't')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT get_bit(E'a'::bytea, 6) = 1 AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == 't')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT get_bit(E'a'::bytea, 7) = 0 AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == 't')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT get_bit(E'josejosejose'::bytea, 94) AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '1')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT get_bit(E'\\x5402036d6173'::bytea, 28)  AS RESULT; """)
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '1')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT get_bit(E'jose\\\\\\000\\\\\\000\\\\\\0000jose\\\\\\00000\\\\\\000000jose'::bytea, 58) AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '0')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT get_bit(E'josejosejose'::bytea, 94) AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '1')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT get_bit(lpad('open', 5000, 'gauss')::bytea, 94) AS RESULT; """)
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '1')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT get_bit(left('ABCDEFGHIJK', 6)::bytea, 44) AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '0')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT get_bit(set_byte(overlay(E'Th\\\\\\000omas'::bytea placing E'\\\\\\002\\\\\\003'::bytea from 2 for 3), 4, 64), 44) AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '1')

    def tearDown(self):
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)
        logger.info('------------------------Opengauss_Function_Binarystring_Get_Bit_Case0001执行结束--------------------------')