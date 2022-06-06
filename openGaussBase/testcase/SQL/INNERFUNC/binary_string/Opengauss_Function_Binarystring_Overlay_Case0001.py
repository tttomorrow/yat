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
Case Name： overlay入参长度关系校验
Descption:overlay(string placing string from int [for int])替换子串

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.overlay的for和from关系校验
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
        logger.info("------------------------Opengauss_Function_Binarystring_Overlay_Case0001开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_overlay(self):

        logger.info("-----------from、for是小数四舍五入-----------")
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("""SELECT overlay('helloworld ' placing ' opengauss ' from 1.5 for 3.5) AS RESULT;""")
        logger.info(Normal_SqlMdg1)
        self.assertTrue(Normal_SqlMdg1.splitlines()[2].strip(' ') == 'h opengauss world')

        logger.info("-----------for<len(s)-from覆盖选中的for个-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""SELECT overlay('helloworld ' placing ' opengauss ' from 3 for 3) AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[2].strip(' ') == 'he opengauss world')

        logger.info("-----------for>len(s)-from全覆盖-----------")
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""SELECT overlay('helloworld ' placing ' opengauss ' from 21/3 for 9) AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[2].strip(' ') == 'hellow opengauss')

        logger.info("-----------for是0直接插入-----------")
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""SELECT overlay('helloworld ' placing ' opengauss ' from 7 for false) AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[2].strip(' ') == 'hellow opengauss orld')

        logger.info("-----------for<0from右边保留for个-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""SELECT overlay('helloworld ' placing ' opengauss ' from 7 for -1) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[2].strip(' ') == 'hellow opengauss world')
        Normal_SqlMdg6 = self.commonsh.execut_db_sql("""SELECT overlay('helloworld ' placing ' opengauss ' from 7 for -2-1) AS RESULT;""")
        logger.info(Normal_SqlMdg6)
        self.assertTrue(Normal_SqlMdg6.splitlines()[2].strip(' ') == 'hellow opengauss loworld')

    def tearDown(self):

        logger.info('------------------------Opengauss_Function_Binarystring_Overlay_Case0001执行结束--------------------------')