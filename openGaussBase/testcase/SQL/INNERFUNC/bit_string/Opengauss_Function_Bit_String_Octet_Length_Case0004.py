'''

Case Type： 功能测试
Case Name： 位串作为octet_length函数的入参(入参为位串操作符或函数的返回结果)
Descption:

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境删除表防止新建失败
步骤 3.入参为操作符或函数操作后的位串
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
        logger.info("------------------------Opengauss_BaseFunc_bit_string_octet_length_004开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_bit_string_in_octet_length(self):
        logger.info("-----------位串操作符或者函数返回值-----------")
        sql_cmd = '''SELECT octet_length(B'10001' || B'011' || (B'10001' & B'01101'));'''
        Normal_SqlMdg = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg.splitlines()[2]) == 2)
        sql_cmd = '''SELECT octet_length(B'1000111111' || (B'011' || B'10001' & B'11101101') <<3);'''
        Normal_SqlMdg = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg.splitlines()[2]) == 3)
        sql_cmd = '''SELECT octet_length(substring('10101111'::bit(8), 2));'''
        Normal_SqlMdg = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg.splitlines()[2]) == 1)
        sql_cmd = '''SELECT octet_length(substring('10101111'::bit(8), octet_length(substring('10101111'::bit(8), 2))));'''
        Normal_SqlMdg = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg.splitlines()[2]) == 1)

    def tearDown(self):
        logger.info('------------------------Opengauss_BaseFunc_bit_string_octet_length_004执行结束--------------------------')