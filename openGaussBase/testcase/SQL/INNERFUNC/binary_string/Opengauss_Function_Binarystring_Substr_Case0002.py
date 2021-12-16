'''

Case Type： 功能测试
Case Name： substr入参异常校验报错
Descption:substr(string, from int [, for int])截取子串。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.substr的入参异常进行报错校验
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
        logger.info("------------------------Opengauss_Function_Binarystring_Substr_Case0002开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_substr(self):

        logger.info("-----------string不支持-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT substr(empty_blob() , 2 , 3) AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue('does not exist' in Normal_SqlMdg2)
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT substr(B'10110' , 2 , 3) AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue('does not exist' in Normal_SqlMdg2)

        logger.info("----------from超范围-----------")
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT substr(E'Th\\\\\\000omas'::bytea , -8888888899999999 , 3) AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.find('ERROR:  function substr(bytea, bigint, integer) does not exist') > -1)

        logger.info("-----------for超范围-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT substr(E'Th\\\\\\000omas'::bytea , 3 , 99999999999999999) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.find('ERROR:  function substr(bytea, integer, bigint) does not exist') > -1)

        logger.info("-----------for 是负数不报错，不同于pg,是为了适配Oracle和MySQL-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT substr(E'Th\\\\\\000omas'::bytea , 1 , -3.6) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[2].strip() == '')

        logger.info("-----------多参、少参、空值-----------")
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""SELECT substr(E'Th\\\\\\000omas'::bytea, 45, 1, 121) AS RESULT;""")
        logger.info(Normal_SqlMdg6)
        self.assertTrue(Normal_SqlMdg6.find('ERROR:  function substr(bytea, integer, integer, integer) does not exist') > -1)
        Normal_SqlMdg7 = self.commonsh.execut_db_sql("""SELECT substr(from 45,for 0) AS RESULT;""")
        logger.info(Normal_SqlMdg7)
        self.assertTrue(Normal_SqlMdg7.find('ERROR:  syntax error') > -1)
        Normal_SqlMdg8 = self.commonsh.execut_db_sql("""SELECT substr(E'Th\\\\\\000omas'::bytea,  , 255) AS RESULT;""")
        logger.info(Normal_SqlMdg8)
        self.assertTrue(Normal_SqlMdg8.find('ERROR:  syntax error') > -1)
        Normal_SqlMdg9 = self.commonsh.execut_db_sql("""SELECT substr(E'Th\\\\\\000omas'::bytea, 5, ) AS RESULT;""")
        logger.info(Normal_SqlMdg9)
        self.assertTrue(Normal_SqlMdg9.find('ERROR:  syntax error') > -1)
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("""SELECT substr(E''::bytea, 5,  0) AS RESULT;""")
        logger.info(Normal_SqlMdg1)
        self.assertTrue(Normal_SqlMdg1.splitlines()[2].strip() == '')

    def tearDown(self):

        logger.info('------------------------Opengauss_Function_Binarystring_Substr_Case0002执行结束--------------------------')