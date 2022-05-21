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
"""
Case Type   : 功能测试
Case Name   : overlay入参异常报错校验
Description : overlay(string placing string from int [for int])替换子串
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境，设置参数
    步骤 3.overlay的入参异常进行报错校验
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


class Bit_string_function(unittest.TestCase):

    def setUp(self):
        logger.info("------------Opengauss_Function_Bit_String_Overlay_Case0002 开始执行--------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh = CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_overlay(self):
        logger.info("-----------from<=0-----------")
        Msg2 = self.commonsh.execut_db_sql(
            """SELECT overlay('hello world' placing 'great opengauss' from -7 for 9) AS RESULT;""")
        logger.info(Msg2)
        self.assertTrue(Msg2.splitlines()[0].strip(' ') == 'ERROR:  negative substring length not allowed')
        Msg3 = self.commonsh.execut_db_sql(
            """SELECT overlay('hello world' placing 'great opengauss' from 0 for 9) AS RESULT;""")
        logger.info(Msg3)
        self.assertTrue(Msg3.splitlines()[0].strip(' ') == 'ERROR:  negative substring length not allowed')

        logger.info("-----------不能替换的-----------")
        Msg4 = self.commonsh.execut_db_sql(
            """SELECT overlay(lpad('open', 50, 'gauss') placing E'\x5402036d6173'::bytea from 1 for 4) AS RESULT;""")
        logger.info(Msg4)
        self.assertTrue('overlay(text, bytea, integer, integer) does not exist' in Msg4)

        logger.info("-----------缺少关键字-----------")
        Msg5 = self.commonsh.execut_db_sql("""SELECT overlay('helloworld '  ' opengauss ' from 3 for 3) AS RESULT;""")
        logger.info(Msg5)
        self.assertTrue('ERROR:  syntax error' in Msg5)

        logger.info("-----------多参、少参、空值-----------")
        Msg6 = self.commonsh.execut_db_sql(
            """SELECT overlay('hello world','hello world' placing 'great opengauss' from 1 for 9) AS RESULT;""")
        logger.info(Msg6)
        self.assertTrue('ERROR:  syntax error' in Msg6)
        Msg7 = self.commonsh.execut_db_sql("""SELECT overlay('hello world' placing  from 1 for 9) AS RESULT;""")
        logger.info(Msg7)
        self.assertTrue('ERROR:  syntax error' in Msg7)
        Msg8 = self.commonsh.execut_db_sql("""SELECT overlay('hello world' placing '' from 1 for 9) AS RESULT;""")
        logger.info(Msg8)
        self.assertTrue(Msg8.splitlines()[2].strip() == '')
        Msg9 = self.commonsh.execut_db_sql("""SELECT overlay('' placing 'great opengauss' from 1 for 9) AS RESULT;""")
        logger.info(Msg9)
        self.assertTrue(Msg9.splitlines()[2].strip() == '')

    def tearDown(self):
        logger.info('---------------Opengauss_Function_Bit_String_Overlay_Case0002 执行结束------------------')
