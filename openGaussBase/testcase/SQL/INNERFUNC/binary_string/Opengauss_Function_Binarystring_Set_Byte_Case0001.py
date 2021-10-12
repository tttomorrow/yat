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

Case Type： 功能测试
Case Name： set_byte操作bytea列
Descption:set_byte(string,offset, newvalue)设置字符串中的字节。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.set_byte的入参是二进制字符串列
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

class byte_string_function(unittest.TestCase):

    def setUp(self):
        logger.info("------------------------Opengauss_Function_Binarystring_Position_Case0001开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_set_byte(self):

        Normal_SqlMdg9 = self.commonsh.execut_db_sql("""
                set bytea_output to 'escape';
                SELECT set_byte('young man', 4, 97) AS RESULT;  
                SELECT set_byte('中国', 2, 97) AS RESULT;
                SELECT set_byte(E'Th\\\\\\000omas'::bytea, 4, 64) AS RESULT;
                SELECT set_byte(E'josejosejose'::bytea,11, 255) AS RESULT;
                SELECT set_byte(E'josejosejose'::bytea,11, 256) AS RESULT;
                SELECT set_byte(E'josejosejose'::bytea,11, 511) AS RESULT;
                SELECT set_byte(E'josejosejose'::bytea,11, 512) AS RESULT;
                SELECT set_byte(E'jose\\\\\\000\\\\\\000\\\\\\0000jose\\\\\\00000\\\\\\000000jose'::bytea,22,102) AS RESULT;
                SELECT set_byte(E'\\\\\\000\\\\\\047\\\\\\134\\\\\\001\\\\\\001\\\\\\176'::bytea,4,102) AS RESULT;
                SELECT set_byte(left('ABCDEFGHIJK', 6)::bytea,0,102) AS RESULT;
                select set_byte(overlay(E'Th\\\\\\000omas'::bytea placing E'\\\\\\002\\\\\\003'::bytea from 2 for 3), 4, 64);""")
        logger.info(Normal_SqlMdg9)
        self.assertTrue(Normal_SqlMdg9.splitlines()[3].strip() == "youna man")
        self.assertTrue(Normal_SqlMdg9.splitlines()[8].strip() == "\\344\\270a\\345\\233\\275")
        self.assertTrue(Normal_SqlMdg9.splitlines()[13].strip() == "Th\\000o@as")
        self.assertTrue(Normal_SqlMdg9.splitlines()[18].strip() == "josejosejos\\377")
        self.assertTrue(Normal_SqlMdg9.splitlines()[23].strip() == "josejosejos\\377")
        self.assertTrue(Normal_SqlMdg9.splitlines()[28].strip() == "josejosejos\\000")
        self.assertTrue(Normal_SqlMdg9.splitlines()[33].strip() == "josejosejos\\377")
        self.assertTrue(Normal_SqlMdg9.splitlines()[38].strip() == "josejosejos\\000")
        self.assertTrue(Normal_SqlMdg9.splitlines()[43].strip() == "jose\\000\\000\\0000jose\\00000\\000000josf")
        self.assertTrue(Normal_SqlMdg9.splitlines()[48].strip() == "\\000'\\\\\\001f~")
        self.assertTrue(Normal_SqlMdg9.splitlines()[53].strip() == "fBCDEF")
        self.assertTrue(Normal_SqlMdg9.splitlines()[58].strip() == "T\\002\\003m@s")

    def tearDown(self):
        SqlMdg2 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg2)
        logger.info('------------------------Opengauss_Function_Binarystring_Position_Case0001执行结束--------------------------')