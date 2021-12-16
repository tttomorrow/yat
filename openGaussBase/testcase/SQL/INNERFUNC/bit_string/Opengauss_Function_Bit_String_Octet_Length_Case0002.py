'''

Case Type： 功能测试
Case Name： 位串作为octet_length函数的入参（参数异常）
Descption:

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境删除表防止新建失败
步骤 3.作入参的位串异常校验
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
        logger.info("------------------------Opengauss_BaseFunc_bit_string_octet_length_002开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_bit_string_in_octet_length(self):
        logger.info("-----------插入数据的长度不符合类型的标准会报错-----------")
        sql_cmd = '''drop table if exists bit_type_t1 ;
                    CREATE TABLE bit_type_t1
                    (
                        BT_COL1 INTEGER,
                        BT_COL2 BIT(3),
                        BT_COL3 BIT VARYING(5)
                    ) ;'''
        self.commonsh.execut_db_sql(sql_cmd)
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("INSERT INTO bit_type_t1 VALUES(2, B'10', B'101');")
        self.assertTrue('ERROR:  bit string length 2 does not match type bit(3)' in Normal_SqlMdg1)
        logger.info("-----------(n)不在范围1-83886080内-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("SELECT octet_length(44::bit(83886081));")
        self.assertTrue('ERROR:  length for type bit cannot exceed 83886080' in Normal_SqlMdg2)

        Normal_SqlMdg3 = self.commonsh.execut_db_sql("SELECT octet_length(B'11110011111001111100'::bit varying(83886081));")
        self.assertTrue('ERROR:  length for type varbit cannot exceed 83886080' in Normal_SqlMdg3)

        Normal_SqlMdg6 = self.commonsh.execut_db_sql("SELECT octet_length(B'11110011111001111100'::bit varying(-1));")
        logger.info(Normal_SqlMdg6)
        self.assertTrue(Normal_SqlMdg6.find('length for type varbit must be at least 1') > -1)
        Normal_SqlMdg7 = self.commonsh.execut_db_sql("SELECT octet_length(B'11110011111001111100'::bit(0));")
        logger.info(Normal_SqlMdg7)
        self.assertTrue(Normal_SqlMdg7.find('ERROR:  length for type bit must be at least 1') > -1)

        logger.info("-----------非01的数报错-----------")
        Normal_SqlMdg8 = self.commonsh.execut_db_sql("SELECT octet_length(B'00000000000000000000h0000');")
        self.assertTrue('is not a valid binary digit' in Normal_SqlMdg8)
        Normal_SqlMdg9 = self.commonsh.execut_db_sql("SELECT octet_length(B'0000000000030000000000000');")
        self.assertTrue('is not a valid binary digit' in Normal_SqlMdg9)
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("SELECT octet_length(B'111100111110011111F00'::bit varying);")
        self.assertTrue('is not a valid binary digit' in Normal_SqlMdg4)
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("SELECT octet_length(B'1111111111111111111114111111110000000000000000000'::bit(1));")
        self.assertTrue('is not a valid binary digit' in Normal_SqlMdg5)

    def tearDown(self):
        clear_sql = 'DROP table IF EXISTS bit_type_t1;'
        self.commonsh.execut_db_sql(clear_sql)
        logger.info('------------------------Opengauss_BaseFunc_bit_string_octet_length_002执行结束--------------------------')