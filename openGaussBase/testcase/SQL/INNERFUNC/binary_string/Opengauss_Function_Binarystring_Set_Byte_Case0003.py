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
Case Name： set_byte操作bytea列
Descption:set_byte(string,offset, newvalue)设置字符串中的字节。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.set_byte的入参是二进制字符串列
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
        logger.info("------------------------Opengauss_Function_Binarystring_Position_Case0003开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_set_byte(self):
        logger.info("--------------------------------参数是列-------------------------------")
        sql_cmd1 = '''drop table if exists test;
                        create table test(c1 text,c2 bytea,c3 bytea);
                        declare
                        begin
                            for i in 1..5000 loop
                            end loop;
                        end;'''
        cmd1 = self.commonsh.execut_db_sql(sql_cmd1)
        logger.info(cmd1)

        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
                                                        SELECT set_byte(c2,5,521-255) from test where rownum < 5;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[3].strip(' ') == 'T0203\\012d6173')
        self.assertTrue(Normal_SqlMdg2.splitlines()[4].strip(' ') == 'Th\\000om\\012sffdfdfdfdfd')
        self.assertTrue(Normal_SqlMdg2.splitlines()[3] == Normal_SqlMdg2.splitlines()[5])
        self.assertTrue(Normal_SqlMdg2.splitlines()[4] == Normal_SqlMdg2.splitlines()[6])

        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT set_byte(c3,7,64) from test where  rownum < 5;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[3].strip(' ') == 'Th\\000omas@fdfdfdfdfd')
        self.assertTrue(Normal_SqlMdg3.splitlines()[4].strip(' ') == "T02036d@173")
        self.assertTrue(Normal_SqlMdg3.splitlines()[3] == Normal_SqlMdg3.splitlines()[5])
        self.assertTrue(Normal_SqlMdg3.splitlines()[4] == Normal_SqlMdg3.splitlines()[6])

    def tearDown(self):
        SqlMdg2 = self.commonsh.execut_db_sql('''drop table test cascade;
                                        set bytea_output to 'hex';''')
        logger.info(SqlMdg2)
        logger.info('------------------------Opengauss_Function_Binarystring_Position_Case0003执行结束--------------------------')