'''

Case Type： 功能测试
Case Name： substr入参正常对非bytea进行截取
Descption:substr(string, from int [, for int])截取子串。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.substr的入参是非二进制字符串
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
        logger.info("------------------------Opengauss_Function_Binarystring_Substr_Case0004开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_substr(self):

        logger.info("----------非bytea-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT substr('young man',4,90);""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[2].strip(' ') == 'ng man')
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT substr(999-888 , 2 , true) AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[2].strip(' ') == '1')
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT substr('中国人' , 1 , 300) AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[2].strip(' ') == '中国人')
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT substr(lpad('open', 5000, 'gauss'),4,5);""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[2].strip(' ') == 'ssgau')
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("""SELECT substr(rawcat(left('ABCDEFGHIJK', 6)::RAW,'0123456789'::RAW),4,5);""")
        logger.info(Normal_SqlMdg1)
        self.assertTrue(Normal_SqlMdg1.splitlines()[2].strip(' ') == 'DEF01')
        Normal_SqlMdg0 = self.commonsh.execut_db_sql("""SELECT substr(reverse(to_char(interval '15h 2m 12s', 'HH24:MI:SS')),4,5);""")
        logger.info(Normal_SqlMdg0)
        self.assertTrue(Normal_SqlMdg0.splitlines()[2].strip(' ') == '20:51')

    def tearDown(self):

        logger.info('------------------------Opengauss_Function_Binarystring_Substr_Case0004执行结束--------------------------')