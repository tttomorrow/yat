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
Case Name： substring入参异常进行报错校验
Descption:substring(string [from int] [for int])截取子串。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.substring入参异常
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
        logger.info("------------------------Opengauss_Function_Binarystring_Substring_Case0002开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_substring(self):

        logger.info("-----------string不支持-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT substring(empty_blob() from 2 for 3) AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue('ERROR:  function pg_catalog.substring(blob, integer, integer) does not exist' in Normal_SqlMdg2)

        logger.info("----------from超范围-----------")
        logger.info(Normal_SqlMdg4)
        self.assertTrue('ERROR:  function pg_catalog.substring(bytea, bigint, integer) does not exist' in Normal_SqlMdg4)

        logger.info("-----------for超范围-----------")
        logger.info(Normal_SqlMdg5)
        self.assertTrue('ERROR:  function pg_catalog.substring(bytea, integer, bigint) does not exist' in Normal_SqlMdg5)

        logger.info("-----------for 是负数报错-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT substring(E'Th\\\\\\000omas'::bytea from 1 for -3.6) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue('ERROR:  negative substring length not allowed' in Normal_SqlMdg5)

        logger.info("-----------多参、少参、空值-----------")
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""SELECT substring(E'Th\\\\\\000omas'::bytea from 45 from 1 for 121) AS RESULT;""")
        logger.info(Normal_SqlMdg6)
        self.assertTrue('ERROR:  syntax error' in Normal_SqlMdg6)
        Normal_SqlMdg7 = self.commonsh.execut_db_sql("""SELECT substring(from 45 for 0) AS RESULT;""")
        logger.info(Normal_SqlMdg7)
        self.assertTrue('ERROR:  syntax error' in Normal_SqlMdg7)
        Normal_SqlMdg8 = self.commonsh.execut_db_sql("""SELECT substring(E'Th\\\\\\000omas'::bytea from for 255) AS RESULT;""")
        logger.info(Normal_SqlMdg8)
        self.assertTrue('ERROR:  syntax error' in Normal_SqlMdg8)
        Normal_SqlMdg9 = self.commonsh.execut_db_sql("""SELECT substring(E'Th\\\\\\000omas'::bytea from 5 for ) AS RESULT;""")
        logger.info(Normal_SqlMdg9)
        self.assertTrue('ERROR:  syntax error' in Normal_SqlMdg9)
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("""SELECT substring(E''::bytea from 5 for 0) AS RESULT;""")
        logger.info(Normal_SqlMdg1)
        self.assertTrue(Normal_SqlMdg1.splitlines()[2].strip(' ') == '')

    def tearDown(self):
        logger.info('------------------------Opengauss_Function_Binarystring_Substring_Case0002执行结束--------------------------')