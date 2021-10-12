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
Case Name   : btrim入参为普通字符串、二进制字符串
Description : btrim(string bytea,bytes bytea)从string的开头和结尾删除只包含bytes中字节的最长的字符串。
    步骤 1.清理环境，设置参数
    步骤 2.btrim入参为普通字符串、二进制字符串
Expect      : 
    步骤 1. 环境清理成功
    步骤 2. 函数返回结果正确
History     : 
"""

import unittest
from yat.test import macro
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Bit_string_function(unittest.TestCase):

    def setUp(self):
        logger.info("--------------Opengauss_Function_Binarystring_Btrim_Case0001开始执行-----------------")
        self.commonsh = CommonSH('dbuser')

    def testbtrim(self):
        logger.info("-----------普通字符串-----------")
        msg1 = self.commonsh.execut_db_sql("""SELECT btrim('opengauss', ' o') AS RESULT;""")
        logger.info(msg1)
        self.assertTrue(msg1.splitlines()[2].strip(' ') == 'pengauss')
        msg2 = self.commonsh.execut_db_sql("""SELECT btrim(12345 , 15) AS RESULT;""")
        logger.info(msg2)
        self.assertTrue(msg2.splitlines()[2].strip(' ') == '234')
        msg3 = self.commonsh.execut_db_sql("""SELECT btrim('小红和小刚' , '小小小') AS RESULT;""")
        logger.info(msg3)
        self.assertTrue(msg3.splitlines()[2].strip(' ') == '红和小刚')

        logger.info("-----------二进制字符串-----------")
        msg4 = self.commonsh.execut_db_sql("""SELECT btrim(' opengauss ', E'\\\\\\000'::bytea) AS RESULT;""")
        logger.info(msg4)
        msg5 = self.commonsh.execut_db_sql("""SELECT btrim('00\\\\\\',E'\\\\\\000'::bytea ) AS RESULT;""")
        logger.info(msg5)
        self.assertTrue(msg5.splitlines()[2].strip(' ') == '\\x30305c')
        msg6 = self.commonsh.execut_db_sql("""SELECT btrim(HEXTORAW('3DEADBEEF'), '12nmg') AS RESULT;""")
        logger.info(msg6)
        self.assertTrue(msg6.splitlines()[2].strip(' ') == '03DEADBEEF')
        msg7 = self.commonsh.execut_db_sql(
            """SELECT btrim(E'\\\\\\000Tom\\\\\\000'::bytea , E'\\\\\\000'::bytea) AS RESULT;""")
        logger.info(msg7)
        self.assertTrue(msg7.splitlines()[2].strip(' ') == '\\x546f6d')

    def tearDown(self):
        logger.info('------------------Opengauss_Function_Binarystring_Btrim_Case0001执行结束--------------')
