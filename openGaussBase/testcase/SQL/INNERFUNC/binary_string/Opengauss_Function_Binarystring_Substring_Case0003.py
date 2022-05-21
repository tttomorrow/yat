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
Case Name： substring对列进行操作
Descption:substring(string [from int] [for int])截取子串。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.substring入参是列
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
        logger.info("------------------------Opengauss_Function_Binarystring_Substring_Case0003开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_substr(self):

        logger.info("--------------------------------参数是列-------------------------------")
        sql_cmd1 = '''drop table if exists test;
                        create table test(c1 text,c2 bytea,c3 bytea);
                        declare
                        begin
                            for i in 1..5000 loop
                                insert into test values('opengauss', E'\\x5402036d6173', E'Th\\\\\\000omasffdfdfdfdfd');
                                insert into test values('opengauss', E'Th\\\\\\000omasffdfdfdfdfd', E'\\x5402036d6173');
                            end loop;
                        end;'''
        cmd1 = self.commonsh.execut_db_sql(sql_cmd1)
        logger.info(cmd1)

        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT substring(c1 from 1 for 9) from test where rownum < 5;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[5].strip(' ') == 'opengauss')

        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT substring(c2 from 2 for 3) from test where rownum < 5;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[2].strip(' ') == "\\x303230")
        self.assertTrue(Normal_SqlMdg3.splitlines()[5].strip(' ') == "\\x68006f")

        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT substring(c1 from 2 for 3) from test where rownum < 5;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[5].strip(' ') == "pen")

    def tearDown(self):
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""drop table if exists test;""")
        logger.info(Normal_SqlMdg5)
        logger.info('------------------------Opengauss_Function_Binarystring_Substring_Case0003执行结束--------------------------')