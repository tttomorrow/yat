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
Case Name： set_bit操作bytea
Descption:set_bit(string,offset, newvalue)设置字符串中的位。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.set_bit的入参是二进制字符串
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
        logger.info("------------------------Opengauss_Function_Binarystring_Set_Bit_Case0001开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_set_bit(self):

        logger.info("-----------bytea-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT set_bit(E'a'::bytea, 0,0) AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[2].strip() == '\\x60')
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT set_bit(E'a'::bytea, 6,0) AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[2].strip() == '\\x21')
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT set_bit(E'a'::bytea, 7,1) AS RESULT; """)
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[2].strip() == '\\xe1')
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""SELECT set_bit(E'josejosejose'::bytea, 39,1) AS RESULT; """)
        logger.info(Normal_SqlMdg6)
        self.assertTrue(Normal_SqlMdg6.splitlines()[2].strip() == '\\x6a6f7365ea6f73656a6f7365')

        Normal_SqlMdg9 = self.commonsh.execut_db_sql("""
        set bytea_output to 'escape';
        SELECT set_bit(E'\\x5402036d6173'::bytea, 28,0)  AS RESULT;
        SELECT set_bit(E'jose\\\\\\000\\\\\\000\\\\\\0000jose\\\\\\00000\\\\\\000000jose'::bytea, 58,1) AS RESULT;
        SELECT set_bit(E'josejosejose'::bytea, 94,0) AS RESULT;
        SELECT set_bit(lpad('open', 50, 'gauss')::bytea, 94,0) AS RESULT;
        sELECT set_bit(convert_to_nocase('12345', 'GBK'), 4,0)  AS RESULT;
        SELECT set_bit(left('ABCDEFGHIJK', 6)::bytea, 1,0) AS RESULT;
        SELECT set_bit(left('ABCDEFGHIJK', 6)::bytea, 1,1) AS RESULT;
        SELECT set_bit(overlay(E'Th\\\\\\000omas'::bytea placing E'\\\\\\002\\\\\\003'::bytea from 2 for 3), 1,0)AS RESULT;
        SELECT set_bit(overlay(E'Th\\\\\\000omas'::bytea placing E'\\\\\\002\\\\\\003'::bytea from 2 for 3), 1,1)AS RESULT;""")
        logger.info(Normal_SqlMdg9)
        self.assertTrue(Normal_SqlMdg9.splitlines()[3].strip() == "T02 36d6173")
        self.assertTrue(Normal_SqlMdg9.splitlines()[8].strip() == "jose\\000\\000\\0004jose\\00000\\000000jose")
        self.assertTrue(Normal_SqlMdg9.splitlines()[13].strip() == "josejosejos%")
        self.assertTrue(Normal_SqlMdg9.splitlines()[18].strip() == "gaussgaussg!ussgaussgaussgaussgaussgaussgaussgopen")
        self.assertTrue(Normal_SqlMdg9.splitlines()[23].strip() == "!2345")
        self.assertTrue(Normal_SqlMdg9.splitlines()[28].strip() == "ABCDEF")
        self.assertTrue(Normal_SqlMdg9.splitlines()[33].strip() == "CBCDEF")
        self.assertTrue(Normal_SqlMdg9.splitlines()[38].strip() == "T\\002\\003mas")
        self.assertTrue(Normal_SqlMdg9.splitlines()[43].strip() == "V\\002\\003mas")

    def tearDown(self):
        SqlMdg2 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg2)
        logger.info('------------------------Opengauss_Function_Binarystring_Set_Bit_Case0001执行结束--------------------------')