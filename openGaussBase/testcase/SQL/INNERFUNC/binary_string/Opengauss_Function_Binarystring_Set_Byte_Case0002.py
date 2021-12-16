'''

Case Type： 功能测试
Case Name： set_byte入参异常报错校验
Descption:set_byte(string,offset, newvalue)设置字符串中的字节。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.set_byte的入参异常进行报错校验
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
        logger.info("------------------------Opengauss_Function_Binarystring_Position_Case0002开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_set_byte(self):

        logger.info("-----------string不支持-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT set_byte(988+89, 2, 97) AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue('function set_byte(integer, integer, integer) does not exist' in Normal_SqlMdg2)

        logger.info("-----------offset超范围-----------")
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT set_byte(E'Th\\\\\\000omas'::bytea, 999999, 0) AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.find("ERROR:  index 999999 out of valid range, 0..6") > -1)

        logger.info("-----------newvalue非int4-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT set_byte('young man', 4, 9999999999999) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.find("ERROR:  function set_byte(unknown, integer, bigint) does not exist") > -1)

        logger.info("-----------多参、少参、空值-----------")
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""SELECT set_byte(E'Th\\\\\\000omas'::bytea, 45,1,121) AS RESULT;""")
        logger.info(Normal_SqlMdg6)
        self.assertTrue(Normal_SqlMdg6.find('does not exist') > -1)
        Normal_SqlMdg7 = self.commonsh.execut_db_sql("""SELECT set_byte( 45, 0) AS RESULT;""")
        logger.info(Normal_SqlMdg7)
        self.assertTrue(Normal_SqlMdg7.find('does not exist') > -1)
        Normal_SqlMdg8 = self.commonsh.execut_db_sql("""SELECT set_byte(E'Th\\\\\\000omas'::bytea, , 255) AS RESULT;""")
        logger.info(Normal_SqlMdg8)
        self.assertTrue(Normal_SqlMdg8.find('ERROR:  syntax error') > -1)
        Normal_SqlMdg9 = self.commonsh.execut_db_sql("""SELECT set_byte(E'Th\\\\\\000omas'::bytea, 5, ) AS RESULT;""")
        logger.info(Normal_SqlMdg9)
        self.assertTrue(Normal_SqlMdg9.find('ERROR:  syntax error') > -1)
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("""SELECT set_byte(E''::bytea, 5, 0) AS RESULT;""")
        logger.info(Normal_SqlMdg1)
        self.assertTrue(Normal_SqlMdg1.splitlines()[2].strip() == '')

    def tearDown(self):

        logger.info('------------------------Opengauss_Function_Binarystring_Position_Case0002执行结束--------------------------')