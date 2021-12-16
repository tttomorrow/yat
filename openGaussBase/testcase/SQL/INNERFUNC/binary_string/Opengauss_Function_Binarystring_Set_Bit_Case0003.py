'''

Case Type： 功能测试
Case Name： set_bit操作bytea列
Descption:set_bit(string,offset, newvalue)设置字符串中的位。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.set_bit的入参是二进制字符串列
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
        logger.info("------------------------Opengauss_Function_Binarystring_Set_Bit_Case0003开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_set_bit(self):
        logger.info("--------------------------------参数是列-------------------------------")
        sql_cmd1 = '''drop table if exists test;
                    create table test(c1 text,c2 bytea,c3 bytea);
                    declare
                    begin
                        for i in 1..1000 loop
                            insert into test values('opengauss', E'\\x5402036d6173', E'Th\\\\\\000omasffdfdfdfdfd');
                            insert into test values('opengauss', E'Th\\\\\\000omasffdfdfdfdfd', E'\\x5402036d6173');
                        end loop;
                    end;'''
        cmd1 = self.commonsh.execut_db_sql(sql_cmd1)
        logger.info(cmd1)

        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
                                                        SELECT set_bit(c2,4,true) from test where rownum < 5;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[3].strip(' ') == 'T02036d6173')
        self.assertTrue(Normal_SqlMdg2.splitlines()[4].strip(' ') == 'Th\\000omasffdfdfdfdfd')
        self.assertTrue(Normal_SqlMdg2.splitlines()[6] == Normal_SqlMdg2.splitlines()[4])
        self.assertTrue(Normal_SqlMdg2.splitlines()[3] == Normal_SqlMdg2.splitlines()[5])


        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
                                                        SELECT set_bit(set_byte(c3, 4, 64),6,2-1) from test where rownum < 5;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[3].strip(' ') == 'Th\\000o@asffdfdfdfdfd')
        self.assertTrue(Normal_SqlMdg3.splitlines()[4].strip(' ') == "T020@6d6173")
        self.assertTrue(Normal_SqlMdg3.splitlines()[3] == Normal_SqlMdg3.splitlines()[5])
        self.assertTrue(Normal_SqlMdg3.splitlines()[4] == Normal_SqlMdg3.splitlines()[6])

    def tearDown(self):
        SqlMdg2 = self.commonsh.execut_db_sql('''drop table test cascade;
                                        set bytea_output to 'hex';''')
        logger.info(SqlMdg2)
        logger.info('------------------------Opengauss_Function_Binarystring_Set_Bit_Case0003执行结束--------------------------')