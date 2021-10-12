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
Case Name： substring对非bytea字符串进行截取
Descption:substring(string [from int] [for int])截取子串。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.substring入参是非bytea
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
        logger.info("------------------------Opengauss_Function_Binarystring_Substring_Case0004开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_substr(self):

        logger.info("----------非bytea-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT substring('young man',4,90);""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[2].strip(' ') == 'ng man')
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT substring(999-888 from 2 for 3) AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[2].strip(' ') == '11')
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT substring('中国人' from 1 for 30) AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[2].strip(' ') == '中国人')
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT substring(B'10110' from 2 for 3) AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[2].strip(' ') == '011')
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("""SELECT substring(B'10110' from 2 for 9/3) AS RESULT;""")
        logger.info(Normal_SqlMdg1)
        self.assertTrue(Normal_SqlMdg1.splitlines()[2].strip(' ') == '011')
        Normal_SqlMdg0 = self.commonsh.execut_db_sql("""SELECT substring(B'10110' from 2 for true) AS RESULT;""")
        logger.info(Normal_SqlMdg0)
        self.assertTrue(Normal_SqlMdg0.splitlines()[2].strip(' ') == '0')
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""SELECT substring(lpad('open', 5000, 'gauss'),4,5);""")
        logger.info(Normal_SqlMdg6)
        self.assertTrue(Normal_SqlMdg6.splitlines()[2].strip(' ') == 'ssgau')
        logger.info(Normal_SqlMdg7)
        self.assertTrue(Normal_SqlMdg7.splitlines()[2].strip(' ') == 'DEF01')
        Normal_SqlMdg8 = self.commonsh.execut_db_sql("""SELECT substring(reverse(to_char(interval '15h 2m 12s', 'HH24:MI:SS')),4,5);""")
        logger.info(Normal_SqlMdg8)
        self.assertTrue(Normal_SqlMdg8.splitlines()[2].strip(' ') == '20:51')

    def tearDown(self):

        logger.info('------------------------Opengauss_Function_Binarystring_Substring_Case0004执行结束--------------------------')