"""
Case Type   : 功能测试
Case Name   : position函数合法值校验
Description : position(substring in string)返回特定子字符串的位置。
    步骤 1. position入参是普通字符串、bytea、函数
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


class Bit_string_function(unittest.TestCase):

    def setUp(self):
        logger.info(
            "------------------------Opengauss_Function_Binarystring_Position_Case0001开始执行--------------------------")
        self.commonsh = CommonSH('dbuser')

    def test_position(self):
        logger.info("-----------普通字符串-----------")
        msg2 = self.commonsh.execut_db_sql(
            """SELECT position('hello world' in '  hello world!!!!') AS RESULT;""")
        logger.info(msg2)
        self.assertTrue(msg2.splitlines()[2].strip(' ') == '3')
        msg21 = self.commonsh.execut_db_sql("""SELECT position(987 in 123987) AS RESULT;""")
        logger.info(msg21)
        self.assertTrue(msg21.splitlines()[2].strip(' ') == '4')
        msg22 = self.commonsh.execut_db_sql("""SELECT position(1 in 9*9) AS RESULT;""")
        logger.info(msg22)
        self.assertTrue(msg22.splitlines()[2].strip(' ') == '2')
        msg23 = self.commonsh.execut_db_sql("""SELECT position('11' in B'10101100') AS RESULT;""")
        logger.info(msg23)
        self.assertTrue(msg23.splitlines()[2].strip(' ') == '5')
        msg24 = self.commonsh.execut_db_sql("""SELECT position(998::text in 'opengauss998899') AS RESULT;""")
        logger.info(msg24)
        self.assertTrue(msg24.splitlines()[2].strip(' ') == '10')
        msg25 = self.commonsh.execut_db_sql("""SELECT position('中国' in '我是中国人') AS RESULT;""")
        logger.info(msg25)
        self.assertTrue(msg25.splitlines()[2].strip(' ') in ['7', '3'])
        msg25 = self.commonsh.execut_db_sql("""SELECT position('-'::text in date '12-10-2010') AS RESULT;""")
        logger.info(msg25)
        self.assertTrue(msg25.splitlines()[2].strip(' ') == '5')

        logger.info("-----------逃逸格式-----------")
        msg3 = self.commonsh.execut_db_sql(
            """SELECT position(E'\\\\\\000om'::bytea in E'Th\\\\\\000omas'::bytea) AS RESULT;""")
        logger.info(msg3)
        self.assertTrue(msg3.splitlines()[2].strip(' ') == '3')

        logger.info("-----------十六进制-----------")
        msg4 = self.commonsh.execut_db_sql(
            """SELECT position(E'\\x30306a6f7365'::bytea in E'\\x6a6f7365000000306a6f7365003030003030306a6f7365'::bytea) AS RESULT;""")
        logger.info(msg4)
        self.assertTrue(msg4.splitlines()[2].strip() == "13")

        logger.info("-----------十六进制+逃逸格式-----------")
        msg5 = self.commonsh.execut_db_sql(
            """SELECT position(E'\\x6f'::bytea in E'jose\\\\\\000\\\\\\000\\\\\\0000jose\\\\\\00000\\\\\\000000jose'::bytea) AS RESULT;""")
        logger.info(msg5)
        self.assertTrue(msg5.splitlines()[2].strip(' ') == '2')

        logger.info("-----------逃逸格式+十六进制-----------")
        msg3 = self.commonsh.execut_db_sql(
            """SELECT position(E'Th\\\\\\000omas'::bytea in E'\\\\\\x8d5468006f6d61738f'::bytea) AS RESULT;""")
        logger.info(msg3)
        self.assertTrue(msg3.splitlines()[2].strip(' ') == '2')

        logger.info("-----------函数-----------")
        msg4 = self.commonsh.execut_db_sql(
            """SELECT position('opengauss' in lpad('open', 500, 'gauss')) AS RESULT;""")
        logger.info(msg4)
        self.assertTrue(msg4.splitlines()[2].strip() == "0")
        msg41 = self.commonsh.execut_db_sql("""SELECT position('^*' in right('*&^%$%&^*', 100)) AS RESULT;""")
        logger.info(msg41)
        self.assertTrue(msg41.splitlines()[2].strip() == '8')
        msg42 = self.commonsh.execut_db_sql(
            """SELECT position(rawcat(left('ABCDEFGHIJK', 6)::RAW,'0123456789'::RAW) in '908U8ABCDEF0123456789') AS RESULT;""")
        logger.info(msg42)
        self.assertTrue(msg42.splitlines()[2].strip() == "6")

        logger.info("-----------不存在-----------")
        msg5 = self.commonsh.execut_db_sql(
            """SELECT position(E'\\\\\\xabcdef'::bytea in E'\\\\\\x98765abc9def3210'::bytea);""")
        logger.info(msg5)
        self.assertTrue(msg5.splitlines()[2].strip(' ') == '0')

    def tearDown(self):
        logger.info(
            '------------------------Opengauss_Function_Binarystring_Position_Case0001执行结束--------------------------')
