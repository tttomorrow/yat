'''

Case Type： 功能测试
Case Name： trim对列进行操作
Descption:trim([both] bytes from string)从string的开头和结尾删除只包含bytes中字节的最长字符串。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.trim入参是列
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
        logger.info("------------------------Opengauss_Function_Binarystring_Trim_Case0003开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_trim(self):

        logger.info("--------------------------------参数是列-------------------------------")
        sql_cmd1 = '''drop table if exists test;
                        create table test(c1 text,c2 bytea,c3 bytea);
                        declare
                        begin
                            for i in 1..5 loop
                                insert into test values('opengauss', E'\\x5402036d6173', E'Th\\\\\\000omasffdfdfdfdfd');
                            end loop;
                        end;'''
        cmd1 = self.commonsh.execut_db_sql(sql_cmd1)
        logger.info(cmd1)
        
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT TRIM(BOTH 'so' from c1) from test;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[5].strip(' ') == 'pengau')

        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT TRIM(BOTH c2 from substring(E'Th\\\\\\000omas'::bytea from 1 for 10)) from test;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[5].strip(' ') == "\\x68006f6d6173")

        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT TRIM(BOTH  E'df' from c3) from test;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[5].strip(' ') == "\\x5468006f6d6173")

    def tearDown(self):
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""drop table if exists test;""")
        logger.info(Normal_SqlMdg5)
        logger.info('------------------------Opengauss_Function_Binarystring_Trim_Case0003执行结束--------------------------')