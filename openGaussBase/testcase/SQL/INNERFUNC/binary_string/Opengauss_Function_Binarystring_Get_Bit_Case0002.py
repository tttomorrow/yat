'''

Case Type： 功能测试
Case Name： get_bit入参异常
Descption:get_bit(string, offset)从字符串中抽取位。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.get_bit入参异常校验报错
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
        logger.info("------------------------Opengauss_Function_Binarystring_Get_Bit_Case0002开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_btrim(self):

        logger.info("-----------超过索引-----------")
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("""SELECT get_bit(E'a'::bytea, 8) = 0 AS RESULT;""")
        logger.info(Normal_SqlMdg1)
        self.assertIn('out of valid range', Normal_SqlMdg1)

        logger.info("-----------非bytea-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT get_bit(right('*&^%$%&^*', 100), 70)  AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertIn('does not exist', Normal_SqlMdg2)
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT get_bit(rawcat(left('ABCDEFGHIJK', 6)::RAW,'0123456789'::RAW), 70)  AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertIn('does not exist', Normal_SqlMdg3)

        logger.info("-----------多参、少参、空值-----------")
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT get_bit(E'a'::bytea, 8, 9) = 0 AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertIn('does not exist', Normal_SqlMdg4)
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT get_bit(, 8) = 0 AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertIn('ERROR:  syntax error', Normal_SqlMdg5)
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""SELECT get_bit(E'a'::bytea, ) = 0 AS RESULT;""")
        logger.info(Normal_SqlMdg6)
        self.assertIn('ERROR:  syntax error', Normal_SqlMdg6)
        Normal_SqlMdg7 = self.commonsh.execut_db_sql("""SELECT get_bit(E''::bytea, 8) = 0 AS RESULT;""")
        logger.info(Normal_SqlMdg7)
        self.assertTrue(Normal_SqlMdg7.splitlines()[2] == ' ')

    def tearDown(self):
        logger.info('------------------------Opengauss_Function_Binarystring_Get_Bit_Case0002执行结束--------------------------')