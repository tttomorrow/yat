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
Case Name   : char_length函数求特殊字符组成的字符串的字符个数
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.入参是特殊字符以及转义字符\
Expect      :
    步骤 1：数据库状态正常
    步骤 2：返回字符个数正确
History     :
"""
import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Length_function(unittest.TestCase):

    def setUp(self):
        logger.info("------------Opengauss_Function_Innerfunc_Char_Length_Add_Case0004开始执行--------------")
        self.commonsh = CommonSH('dbuser')

    def test_function(self):
        logger.info("-------------求特殊字符组成的字符串的字符个数---------------")

        sql_list = [r"""select char_length('~!@#$%^&*');""",
                    r"""select char_length('#%##&^^&//<>\');"""]

        result_list = ['9', '13']
        for i in range(2):
            msg = self.commonsh.execut_db_sql(sql_list[i])
            logger.info(msg)
            self.assertTrue(msg.splitlines()[2].strip() == result_list[i])

    def tearDown(self):
        logger.info('--------------Opengauss_Function_Innerfunc_Char_Length_Add_Case0004执行结束-------------')
