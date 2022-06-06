"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
'''

Case Type： 功能测试
Case Name： btrim入参为其它函数或者列
Descption:btrim(string bytea,bytes bytea)从string的开头和结尾删除只包含bytes中字节的最长的字符串。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.btrim入参为其它函数返回结果，或者列
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
        logger.info("------------------------Opengauss_Function_Binarystring_Btrim_Case0003开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_btrim(self):

        logger.info("-----------------------------与函数交互-------------------------------")
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("""SELECT btrim(E'0134\\\\\\000Tom\\\\\\000'::bytea, left(E'\\\\\\000', 6)::bytea) AS RESULT;""")
        logger.info(Normal_SqlMdg1)
        self.assertTrue(Normal_SqlMdg1.splitlines()[2].strip(' ') == '\\x3031333400546f6d')
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT btrim(lpad(E'0134\\\\\\000Tom\\\\\\000',19,'F')::bytea,left(E'\\\\\\000', 6)::bytea) AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[2].strip(' ') == '\\x464646463031333400546f6d')
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT btrim(set_byte(overlay(E'Th\\\\\\000omas'::bytea placing E'\\\\\\002\\\\\\003'::bytea from 2 for 3), 4, 64),E'\\\\\\000'::bytea) AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[2].strip(' ') == '\\x5402036d4073')

        logger.info("--------------------------------参数是列-------------------------------")
        sql_cmd1 = '''drop table if exists test;
                        create table test(c1 text,c2 bytea,c3 bytea);
                        declare
                        begin
                            for i in 1..5 loop
                                insert into test values('opengauss', E'\\x5402036d6173', E'Th\\\\\\000omasffdfdfdfdfd');
                            end loop;
                        end;
            '''
        cmd1 = self.commonsh.execut_db_sql(sql_cmd1)
        logger.info(cmd1)

        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT btrim(c1 , 'so') from test;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.count('pengau') == 5)
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT btrim(substring(E'Th\\\\\\000omas'::bytea from 1 for 10),c2) from test;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.count('\\x68006f6d6173') == 5)
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT btrim(c3,E'df' ) from test;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.count('\\x5468006f6d6173') == 5)
        Normal_SqlMdg7 = self.commonsh.execut_db_sql("""drop table test cascade;""")
        logger.info(Normal_SqlMdg7)
        self.assertTrue('DROP TABLE' in Normal_SqlMdg7)

    def tearDown(self):
        logger.info('------------------------Opengauss_Function_Binarystring_Btrim_Case0003执行结束--------------------------')