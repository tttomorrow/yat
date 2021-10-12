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
Case Name   : regexp_split_to_array函数参数个数校验
Description : regexp_split_to_table(string text, pattern text [, flags text])用POSIX正则表达式作为分隔符，分隔string。
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.多参、少参、空值、非法值
Expect      :
    步骤 1：数据库状态正常
    步骤 2：除空值外合理报错
History     :
"""
import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Regexp_split_function(unittest.TestCase):

    def setUp(self):
        logger.info("------------Opengauss_Function_Innerfunc_Regexp_Split_To_Table_Case0016开始执行--------------")
        self.commonsh = CommonSH('dbuser')

    def test_function(self):
        logger.info("-------------regexp_split_to_table函数多参、少参、参数非法值及空值的校验--------------")

        sql_list = [r"""SELECT regexp_split_to_table('sweety','sweety', E'\\\s*');""",
                    r"""SELECT regexp_split_to_table('sweety');""",
                    r"""SELECT regexp_split_to_table('sweety',);""",
                    r"""SELECT regexp_split_to_table(,E'\\\s*');""",
                    r"""SELECT regexp_split_to_table('Yes no yes NO YES No yES', 'nO','g');""",
                    r"""SELECT regexp_split_to_table('', E'\\\s*');""",
                    r"""SELECT regexp_split_to_table('sweety', '');""",
                    r"""SELECT regexp_split_to_table(null, E'\\\s*');""",
                    r"""SELECT regexp_split_to_table('sweety', null);"""]

        for i in range(9):
            msg = self.commonsh.execut_db_sql(sql_list[i])
            logger.info(msg)
            if i < 5:
                self.assertTrue('ERROR' in msg)
            else:
                self.assertTrue(msg.splitlines()[2].strip() == '(0 rows)')

    def tearDown(self):
        logger.info('--------------Opengauss_Function_Innerfunc_Regexp_Split_To_Table_Case0016执行结束-------------')
