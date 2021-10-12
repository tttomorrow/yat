"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Name： position对列进行操作
Descption:position(substring in string)特定子字符串的位置。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.position入参是列
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
        logger.info("------------------------Opengauss_Function_Binarystring_Position_Case0003开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_position(self):

        logger.info("--------------------------------参数是列-------------------------------")
        sql_cmd1 = '''drop table if exists test;
                        create table test(c1 text,c2 bytea,c3 bytea,c4 bytea);
                        declare
                        begin
                            for i in 1..5000 loop
                                insert into test values('opengaussTh', E'\\\\\\xabcdef', E'Th\\\\\\000omasffdfdfdfdfd',E'\\\\\\x987654abcdef3210');
                            end loop;
                        end; '''
        cmd1 = self.commonsh.execut_db_sql(sql_cmd1)
        logger.info(cmd1)

        logger.info("-----------列+列-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT position(c2 in c4) from test where rownum <10;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[10].strip(' ') == '4')


        logger.info("-----------列+普通字符串-----------")
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT position('eng' in c1) from test where rownum <3;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[3].strip(' ') == '3')

        logger.info("-----------列+十六进制格式-----------")
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT position('\\x54' in c4) from test where rownum <3;""")
        logger.info(Normal_SqlMdg4)
        logger.info(Normal_SqlMdg4.splitlines()[2].strip())
        self.assertTrue(Normal_SqlMdg4.splitlines()[3].strip() == "3")

        logger.info("-----------列+逃逸格式-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT position(E'\\\\\\000omas'::bytea in c3) from test where rownum <5;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[5].strip(' ') == '3')

    def tearDown(self):
        SqlMdg1 = self.commonsh.execut_db_sql('''drop table test cascade;''')
        logger.info(SqlMdg1)
        logger.info('------------------------Opengauss_Function_Binarystring_Position_Case0003执行结束--------------------------')