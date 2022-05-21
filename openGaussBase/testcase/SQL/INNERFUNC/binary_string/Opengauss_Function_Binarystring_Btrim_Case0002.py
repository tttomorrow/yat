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
Case Name   : btrim入参异常
Description : 描述：btrim(string bytea,bytes bytea)从string的开头和结尾删除只包含bytes中字节的最长的字符串。
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境，设置参数
    步骤 3.btrim多参少参空值异常等校验报错
Expect      : 
    步骤 1：数据库状态正常
    步骤 2：环境清理成功
    步骤 3：异常报错
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
        logger.info("------------------------Opengauss_Function_Binarystring_Btrim_Case0002开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()
        SqlMdg1 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg1)

    def test_btrim(self):

        logger.info("-----------多参-----------")
        Msg1 = self.commonsh.execut_db_sql("""SELECT btrim('anmg','mnag' , 'man young man') AS RESULT;""")
        logger.info(Msg1)
        self.assertIn('does not exist', Msg1)

        logger.info("-----------少参-----------")
        Msg2 = self.commonsh.execut_db_sql("""SELECT btrim('man young man') AS RESULT;""")
        logger.info(Msg2)
        self.assertTrue(Msg2.splitlines()[2].strip(' ') == 'man young man')
        Msg3 = self.commonsh.execut_db_sql("""SELECT btrim(,'man young man') AS RESULT;""")
        logger.info(Msg3)
        self.assertIn('ERROR:  syntax error', Msg3)

        logger.info("-----------空值-----------")
        Msg5 = self.commonsh.execut_db_sql("""SELECT btrim('' ,'saffd') AS RESULT;""")
        logger.info(Msg5)
        self.assertTrue(Msg5.splitlines()[2].strip() == '')
        Msg4 = self.commonsh.execut_db_sql("""SELECT btrim('anmg' ,'') AS RESULT;""")
        logger.info(Msg4)
        self.assertTrue(Msg4.splitlines()[2].strip() == '')

    def tearDown(self):
        logger.info('------------------------Opengauss_Function_Binarystring_Btrim_Case0002执行结束--------------------------')