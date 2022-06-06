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
Case Name： trim操作非bytea字符串
Descption:trim([both] bytes from string)从string的开头和结尾删除只包含bytes中字节的最长字符串。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.trim入参是非bytea
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
        logger.info("------------------------Opengauss_Function_Binarystring_Trim_Case0004开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_substr(self):

        logger.info("----------无参数相当于both-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT trim('anmg' from 'man young man') AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[2].strip(' ') == 'young')
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT trim('ny' from 'young man') AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[2].strip(' ') == 'oung ma')
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT trim('na' from 'man young') AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[2].strip(' ') == 'man young')
        Normal_SqlMdg11 = self.commonsh.execut_db_sql("""SELECT trim(5454 from 12344) AS RESULT;""")
        logger.info(Normal_SqlMdg11)
        self.assertTrue(Normal_SqlMdg11.splitlines()[2].strip(' ') == '123')

        logger.info("----------设定可选参数-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT trim(leading 'man' from 'man young man') AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[2].strip(' ') == 'young man')
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT trim(trailing 'man' from 'man young man') AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[2].strip(' ') == 'man young')
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT trim(both 'man' from 'man young man') AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[2].strip(' ') == 'young')
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT trim('young' from 'man young man') AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[2].strip(' ') == 'man young ma')

        logger.info("----------与其它函数交互-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT trim('^*' from right('*&^%$%&^*', 100)) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[2].strip(' ') == '&^%$%&')
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT trim('s:15' from reverse(to_char(interval '15h 2m 12s', 'HH24:MI:SS'))) AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[2].strip(' ') == '21:20')
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT trim(lpad('open', 5000, 'gauss') from lpad('open', 18, 'gauss')) AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[2].strip() == '')
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT trim(left('HABCDEFGHIJK', 6)::TEXT from rawcat(left('0ABCDEFGHIJK', 6)::RAW,'0123456789'::RAW)::TEXT) AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[2].strip(' ') == '0ABCDE0123456789')

    def tearDown(self):

        logger.info('------------------------Opengauss_Function_Binarystring_Trim_Case0004执行结束--------------------------')