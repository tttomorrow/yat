'''

Case Type： 功能测试
Case Name： get_byte操作二进制列
Descption:get_byte(string, offset)从字符串中抽取字节。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.get_byte入参为二进制列
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
        logger.info("------------------------Opengauss_Function_Binarystring_Get_Byte_Case0003开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_get_byte(self):

        logger.info("--------------------------------参数是列-------------------------------")
        sql_cmd1 = '''drop table if exists test;
                        create table test(c1 text,c2 bytea,c3 bytea);
                        declare
                        begin
                            for i in 1..5000 loop
                                insert into test values('opengauss', E'\\x5402036d6173', E'Th\\\\\\000omasffdfdfdfdfd');
                            end loop;
                        end;
            '''
        cmd1 = self.commonsh.execut_db_sql(sql_cmd1)
        logger.info(cmd1)

        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT get_byte(c2,5) from test where rownum <6;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.count('54') == 5)
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT get_byte(c3,7) from test where rownum <6;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.count('102') == 5)
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT get_byte(c3,7) from test where rownum <256;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.count('102') == 255)

    def tearDown(self):

        SqlMdg1 = self.commonsh.execut_db_sql('''drop table test cascade;''')
        logger.info(SqlMdg1)
        logger.info('------------------------Opengauss_Function_Binarystring_Get_Byte_Case0003执行结束--------------------------')