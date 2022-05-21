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
Case Name： overlay对汉字、数字、二进制等进行交叉替换
Descption:overlay(string placing string from int [for int])替换子串

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.overlay对汉字、数字、二进制等进行交叉替换
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
        logger.info("------------------------Opengauss_Function_Binarystring_Overlay_Case0003开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_overlay(self):

        logger.info("-----------数字-----------")
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("""SELECT overlay(12345 placing 6789 from to_number('6') for 5%5) AS RESULT;""")
        logger.info(Normal_SqlMdg1)
        self.assertTrue(Normal_SqlMdg1.splitlines()[2].strip(' ') == '123456789')

        logger.info("-----------汉字-----------")
        Normal_SqlMdg0 = self.commonsh.execut_db_sql("""SELECT overlay('hello ' placing ' 中国 ' from 1 for 20) AS RESULT;""")
        logger.info(Normal_SqlMdg0)
        self.assertTrue(Normal_SqlMdg0.splitlines()[2].strip(' ') == '中国')

        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to escape;''')
        logger.info(SqlMdg1)

        logger.info("-----------十六进制格式+十六进制格式-----------")
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""set bytea_output to escape;
        SELECT overlay(E'\\x5402036d6173'::bytea placing E'\\x5402036d6173'::bytea from 2 for 3) AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[3].strip() == 'TT02036d617336d6173')

        logger.info("-----------逃逸格式+逃逸格式-----------")
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""set bytea_output to escape;
        SELECT overlay(E'Th\\\\\\000omas'::bytea placing E'\\\\\\002\\\\\\003'::bytea from 2 for 3) AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[3].strip(' ') == 'T\\002\\003mas')

        logger.info("-----------逃逸格式+十六进制格式-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""set bytea_output to escape;
        SELECT overlay(E'\\x5402036d6173'::bytea placing E'Th\\\\\\000omas'::bytea from 2 for 3) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[3].strip(' ') == 'TTh\\000omas36d6173')
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""set bytea_output to escape;
        SELECT overlay(E'Th\\\\\\000omas'::bytea placing E'\\x5402036d6173'::bytea from 2 for 3) AS RESULT;""")
        logger.info(Normal_SqlMdg6)
        self.assertTrue(Normal_SqlMdg6.splitlines()[3].strip(' ') == 'TT02036d6173mas')

        logger.info("-----------函数-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""set bytea_output to escape;
        SELECT overlay(set_byte(overlay(E'Th\\\\\\000omas'::bytea placing E'\\\\\\002\\\\\\003'::bytea from 2 for 3), 4, 64) placing E'\\\\\\005\\\\\\006'::bytea from 2 for 3) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[3].strip(' ') == 'T\\005\\006@s')
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""set bytea_output to escape;
        SELECT overlay(reverse(to_char(interval '15h 2m 12s', 'HH24:MI:SS')) placing '9:8' from 2 for 3) AS RESULT;""")
        logger.info(Normal_SqlMdg6)
        self.assertTrue(Normal_SqlMdg6.splitlines()[3].strip(' ') == '29:80:51')

    def tearDown(self):
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)
        logger.info('------------------------Opengauss_Function_Binarystring_Overlay_Case0003执行结束--------------------------')