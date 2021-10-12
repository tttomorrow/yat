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
Case Name   : quote_literal(value anyelement)函数入参包含反斜杠
Description : 将给定值为文本并且接着将它用引号包围作为一个文本。嵌入的单引号和反斜线被正确的双写
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.入参包含反斜杠
Expect      :
    步骤 1：数据库状态正常
    步骤 2：返回新字符串正确
History     :
"""
import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Lpad_function(unittest.TestCase):

    def setUp(self):
        logger.info("------------Opengauss_Function_Innerfunc_Quote_Literal_Case0008开始执行--------------")
        self.commonsh = CommonSH('dbuser')

    def test_function(self):
        logger.info("-------------•quote_literal(value anyelement)函数入参包含反斜杠---------------")

        sql_list = [r"""SELECT quote_literal(E'O\'42.5');""",
                    r"""SELECT quote_literal(E'O\'\'42.5');""",
                    r"""SELECT quote_literal('O\42.5');""",
                    r"""SELECT quote_literal('O\P\UHGYU\42.5');"""]

        result_list = ["'O''42.5'", "'O''''42.5'", "E'O\\\\42.5'", "E'O\\\\P\\\\UHGYU\\\\42.5'"]

        for i in range(4):
            msg = self.commonsh.execut_db_sql(sql_list[i])
            logger.info(msg)
            self.assertTrue(msg.splitlines()[2].strip() == result_list[i])

    def tearDown(self):
        logger.info('--------------Opengauss_Function_Innerfunc_Quote_Literal_Case0008执行结束-------------')
