'''

Case Type： 功能测试
Case Name： octet_length操作普通字符串、二进制字符串
Descption:octet_length(string)二进制字符串中的字节数。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.octet_length入参为普通字符串、二进制字符串
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
        logger.info("------------------------Opengauss_Function_Binarystring_Octet_Length_Case0001开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_octet_length(self):

        logger.info("-----------非bytea-----------")
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT octet_length('young man');""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '9')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT octet_length(right('*&^%$%&^*', 100));""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '9')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT octet_length(reverse(to_char(interval '15h 2m 12s', 'HH24:MI:SS'))); """)
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '8')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT octet_length(lpad('open', 5000, 'gauss'));""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '5000')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT octet_length(rawcat(left('ABCDEFGHIJK', 6)::RAW,'0123456789'::RAW));""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '16')

        logger.info("-----------二进制字符串bytea-----------")
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT octet_length(E'josejosejose'::bytea) AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '12')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT octet_length(E'\\x5402036d6173') AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '11')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT octet_length(E'jose\\\\\\000\\\\\\000\\\\\\0000jose\\\\\\00000\\\\\\000000jose'::bytea) AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '23')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT octet_length(E'\\\\\\000\\\\\\047\\\\\\134\\\\\\001\\\\\\001\\\\\\176'::bytea) AS RESULT;""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '6')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT octet_length(left('ABCDEFGHIJK', 6)::bytea);""")
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '6')
        Normal_SqlMdg = self.commonsh.execut_db_sql("""SELECT octet_length(set_byte(overlay(E'Th\\\\\\000omas'::bytea placing E'\\\\\\002\\\\\\003'::bytea from 2 for 3), 4, 64)) AS RESULT; """)
        logger.info(Normal_SqlMdg)
        self.assertTrue(Normal_SqlMdg.splitlines()[2].strip(' ') == '6')


    def tearDown(self):

        logger.info('------------------------Opengauss_Function_Binarystring_Octet_Length_Case0001执行结束--------------------------')