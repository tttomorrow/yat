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
Case Name： 位串作为octet_length函数的入参
Descption:

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境删除表防止新建失败
步骤 3.校验位串的结构
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
        logger.info("------------------------Opengauss_BaseFunc_bit_string_octet_length_001开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_bit_string_in_octet_length(self):
        logger.info("-----------B可以省略-----------")
        Normal_SqlMdg = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg.splitlines()[2]) == 1)
        Normal_SqlMdg = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg.splitlines()[2]) == 20)

        logger.info("-----------全0、全1-----------")
        Normal_SqlMdg1 = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg1.splitlines()[2]) == 4)
        sql_cmd = '''SELECT octet_length(B'11111111111111111111111111111');'''
        Normal_SqlMdg1 = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg1.splitlines()[2]) == 4)

        logger.info("-----------数字-----------")
        sql_cmd = '''SELECT octet_length(44::bit(83886080));'''
        Normal_SqlMdg21 = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg21.splitlines()[2]) == 10485760)
        sql_cmd = '''SELECT octet_length(144::bit(33));'''
        Normal_SqlMdg21 = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg21.splitlines()[2]) == 5)

        logger.info("-----------varying(n)-----------")
        Normal_SqlMdg321 = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg321.splitlines()[2]) == 1)
        Normal_SqlMdg321 = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg321.splitlines()[2]) == 3)
        Normal_SqlMdg321 = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg321.splitlines()[2]) == 3)

        logger.info("-----------bit(n)-----------")
        Normal_SqlMdg321 = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg321.splitlines()[2]) == 1)
        Normal_SqlMdg321 = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg321.splitlines()[2]) == 5)
        Normal_SqlMdg321 = self.commonsh.execut_db_sql(sql_cmd)
        self.assertTrue(int(Normal_SqlMdg321.splitlines()[2]) == 1)

    def tearDown(self):

        logger.info('------------------------Opengauss_BaseFunc_bit_string_octet_length_001执行结束--------------------------')