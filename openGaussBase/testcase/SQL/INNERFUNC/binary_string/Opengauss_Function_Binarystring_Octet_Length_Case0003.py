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
Case Name： octet_length操作列
Descption:octet_length(string)二进制字符串中的字节数。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.octet_length入参为普通字符串、二进制字符串的列
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
        logger.info("------------------------Opengauss_Function_Binarystring_Octet_Length_Case0003开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_octet_length(self):

        logger.info("--------------------------------参数是列-------------------------------")
        sql_cmd1 = '''drop table if exists test;
                        create table test(c1 text,c2 bytea,c3 bytea);
                        declare
                        begin
                            for i in 1..5 loop
                            end loop;
                        end;
            '''
        cmd1 = self.commonsh.execut_db_sql(sql_cmd1)
        logger.info(cmd1)
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT octet_length(c1) from test;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.count('9') == 5)
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT octet_length(get_byte(c2, 4)) from test;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.count('2') == 5)
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT octet_length(set_byte(c3, 4, 64)) from test;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.count('18') == 5)

    def tearDown(self):

        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""drop table test cascade;""")
        logger.info(Normal_SqlMdg5)
        logger.info('------------------------Opengauss_Function_Binarystring_Octet_Length_Case0003执行结束--------------------------')