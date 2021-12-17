'''

Case Type： 功能测试
Case Name： octet_length对列进行操作
Descption:overlay(string placing string from int [for int])替换子串

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.overlay入参是列
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
        logger.info("------------------------Opengauss_Function_Binarystring_Overlay_Case0004开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_overlay(self):

        logger.info("--------------------------------参数是列-------------------------------")
        sql_cmd1 = '''drop table if exists test;
                        create table test(c1 text,c2 bytea,c3 bytea);
                        declare
                        begin
                            for i in 1..5 loop
                                insert into test values('opengauss', E'\\x5402036d6173', E'Th\\\\\\000omasffdfdfdfdfd');
                            end loop;
                        end; '''
        cmd1 = self.commonsh.execut_db_sql(sql_cmd1)
        logger.info(cmd1)

        logger.info("-----------列+列-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';SELECT overlay(c2 placing c3 from 4 for 0) from test AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[7].strip(' ') == 'T02Th\\000omasffdfdfdfdfd036d6173')


        logger.info("-----------列+普通字符串-----------")
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';SELECT overlay(c1 placing 'good' from 10 for 5) from test AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[6].strip(' ') == 'opengaussgood')

        logger.info("-----------列+十六进制格式-----------")
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';SELECT overlay(c2 placing E'\\x5d5d5d5d' from 6 for 5) from test AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        logger.info(Normal_SqlMdg4.splitlines()[2].strip())
        self.assertTrue(Normal_SqlMdg4.splitlines()[6].strip() == "T0203]5d5d5d3")

        logger.info("-----------列+逃逸格式-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT overlay(c3 placing E'jose\\\\\\000\\\\\\000\\\\\\0000jose\\\\\\00000\\\\\\000000jose'::bytea from 6 for 5) from test AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[6].strip(' ') == 'Th\\000omjose\\000\\000\\0000jose\\00000\\000000josefdfdfdfd')


    def tearDown(self):
        SqlMdg1 = self.commonsh.execut_db_sql('''drop table test cascade;
                                               set bytea_output to 'hex';''')
        logger.info(SqlMdg1)
        logger.info('------------------------Opengauss_Function_Binarystring_Overlay_Case0004执行结束--------------------------')