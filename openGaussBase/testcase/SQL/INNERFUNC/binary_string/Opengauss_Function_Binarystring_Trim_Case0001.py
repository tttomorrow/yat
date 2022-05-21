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
Case Name   : trim函数对bytea进行截取
Description : trim([both] bytes from string)从string的开头和结尾删除只包含bytes中字节的最长字符串。
    步骤 1.trim的入参是二进制字符串
Expect      : 
    步骤 1. 函数返回结果正确
History     : 
"""
import unittest
from yat.test import macro
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class byte_string_function(unittest.TestCase):

    def setUp(self):
        logger.info(
            "------------------------Opengauss_Function_Binarystring_Trim_Case0001开始执行--------------------------")
        self.commonsh = CommonSH('dbuser')

    def test_trim(self):
        logger.info("-----------二进制字符串-----------")
        msg5 = self.commonsh.execut_db_sql("""SELECT trim(E'\\\\\\000'::bytea from ' opengauss ') AS RESULT;""")
        logger.info(msg5)
        self.assertTrue(msg5.splitlines()[2].strip(' ') == '\\x206f70656e676175737320')
        msg51 = self.commonsh.execut_db_sql("""SELECT trim(E'\\\\\\000'::bytea from '00\\\\\\') AS RESULT;""")
        logger.info(msg51)
        self.assertTrue(msg51.splitlines()[2].strip(' ') == '\\x30305c')
        msg52 = self.commonsh.execut_db_sql("""SELECT trim('12nmg' from HEXTORAW('3DEADBEEF')) AS RESULT;""")
        logger.info(msg52)
        self.assertTrue(msg52.splitlines()[2].strip(' ') == '03DEADBEEF')

        logger.info("-----------不支持只删除左或右，只支持both, 但是both可有可无-----------")
        msg5 = self.commonsh.execut_db_sql(
            """SELECT trim(E'\\\\\\000'::bytea from E'\\\\\\000Tom\\\\\\000'::bytea) AS RESULT;""")
        logger.info(msg5)
        self.assertTrue(msg5.splitlines()[2].strip(' ') == '\\x546f6d')
        msg51 = self.commonsh.execut_db_sql(
            """SELECT trim(both E'\\\\\\000'::bytea from E'\\\\\\000Tom\\\\\\000'::bytea) AS RESULT;""")
        logger.info(msg51)
        self.assertTrue(msg51.splitlines()[2].strip(' ') == '\\x546f6d')
        msg52 = self.commonsh.execut_db_sql(
            """SELECT trim(E'\\x0ACB'::bytea from E'\\\\\\xB0987654524656789BCA'::bytea) AS RESULT;""")
        logger.info(msg52)
        self.assertTrue(msg52.splitlines()[2].strip(' ') == '\\xb0987654524656789bca')
        msg53 = self.commonsh.execut_db_sql(
            """SELECT trim(both E'\\x0ACB'::bytea from E'\\\\\\xB0987654524656789BCA'::bytea) AS RESULT;""")
        logger.info(msg53)
        self.assertTrue(msg53.splitlines()[2].strip(' ') == '\\xb0987654524656789bca')

        logger.info("-----------与其它函数交互-----------")
        msg5 = self.commonsh.execut_db_sql(
            """SELECT trim(both left(E'\\\\\\000', 6)::bytea from E'0134\\\\\\000Tom\\\\\\000'::bytea) AS RESULT;""")
        logger.info(msg5)
        self.assertTrue(msg5.splitlines()[2].strip(' ') == '\\x3031333400546f6d')
        msg51 = self.commonsh.execut_db_sql(
            """SELECT trim(both left(E'\\\\\\000', 6)::bytea from lpad(E'0134\\\\\\000Tom\\\\\\000',19,'F')::bytea) AS RESULT;""")
        logger.info(msg51)
        self.assertTrue(msg51.splitlines()[2].strip(' ') == '\\x464646463031333400546f6d')
        msg52 = self.commonsh.execut_db_sql(
            """SELECT trim(E'\\\\\\000'::bytea from set_byte(overlay(E'Th\\\\\\000omas'::bytea placing E'\\\\\\002\\\\\\003'::bytea from 2 for 3), 4, 64)) AS RESULT;""")
        logger.info(msg52)
        self.assertTrue(msg52.splitlines()[2].strip(' ') == '\\x5402036d4073')

    def tearDown(self):
        logger.info(
            '------------------------Opengauss_Function_Binarystring_Trim_Case0001执行结束--------------------------')
