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
"""
Case Type   : 功能测试
Case Name   : trim入参异常进行报错校验
Description : trim([both] bytes from string)从string的开头和结尾删除只包含bytes中字节的最长字符串。
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境，设置参数
    步骤 3.trim入参异常
Expect      : 
    步骤 1：数据库状态正常
    步骤 2：环境清理成功
    步骤 3：函数返回结果正确，异常输入报错
History     : 
"""
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
        logger.info("----------------Opengauss_Function_Binarystring_Trim_Case0002 开始执行----------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_trim(self):

        logger.info("-----------string不支持-----------")
        Msg2 = self.commonsh.execut_db_sql("""SELECT trim(B'101'from 12344) AS RESULT;""")
        logger.info(Msg2)
        self.assertTrue('ERROR:  function pg_catalog.btrim(integer, bit) does not exist' in Msg2)

        logger.info("----------关键字错误-----------")
        Msg4 = self.commonsh.execut_db_sql("""SELECT trim('anmg'IN 'shuADGHEUU') AS RESULT;""")
        logger.info(Msg4)
        self.assertTrue('ERROR:  syntax error' in Msg4)

        logger.info("-----------多参、少参、空值-----------")
        Msg6 = self.commonsh.execut_db_sql("""SELECT trim('anmg','mnag' from 'man young man') AS RESULT;""")
        logger.info(Msg6)
        self.assertTrue('ERROR:  syntax error' in Msg6)
        Msg7 = self.commonsh.execut_db_sql("""SELECT trim(from 'man young man') AS RESULT;""")
        logger.info(Msg7)
        self.assertTrue('man young man' in Msg7)
        Msg8 = self.commonsh.execut_db_sql("""SELECT trim('anmg' from) AS RESULT;""")
        logger.info(Msg8)
        self.assertTrue('ERROR:  syntax error' in Msg8)
        Msg9 = self.commonsh.execut_db_sql("""SELECT trim('' from 'man young man') AS RESULT;""")
        logger.info(Msg9)
        self.assertTrue(Msg9.splitlines()[2].strip() == '')
        Msg1 = self.commonsh.execut_db_sql("""SELECT trim('anmg'from '') AS RESULT;""")
        logger.info(Msg1)
        self.assertTrue(Msg1.splitlines()[2].strip() == '')

    def tearDown(self):
        logger.info('-------------Opengauss_Function_Binarystring_Trim_Case0002 执行结束----------------')