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
Case Name   : regexp_split_to_table函数对分割匹配的规则的校验
Description : 用POSIX正则表达式作为分隔符，分隔string。
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.全部匹配、部分匹配、零匹配
Expect      :
    步骤 1：数据库状态正常
    步骤 2：如果没有与pattern的匹配，该函数返回string。如果有至少有一个匹配，对每一个匹配它都返回从上一个匹配的末尾
        （或者串的开头）到这次匹配开头之间的文本。当没有更多匹配时，它返回从上一次匹配的末尾到串末尾之间的文本。
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
        logger.info("------------Opengauss_Function_Innerfunc_Regexp_Split_To_Table_Case0009开始执行--------------")
        self.commonsh = CommonSH('dbuser')

    def test_function(self):
        logger.info("-------------regexp_split_to_table函数验证匹配规则---------------")

        sql_list = [r"""SELECT regexp_split_to_table('u can be just the one u wanna be', E'\\\s+');""",
                    r"""SELECT regexp_split_to_table('yo i ran i climb i sar','i ');""",
                    r"""SELECT regexp_split_to_table('u can be just-the-one u-wanna-be', E'\\\s+');""",
                    r"""SELECT regexp_split_to_table('u u u u u u u u i ran i climb i sar  u u u u u u ','i ');""",
                    r"""SELECT regexp_split_to_table('let it go ~ let it go ~ !!!!', 'say it');""",
                    r"""SELECT regexp_split_to_table('hello world', '好');"""]

        result_list = [['u', 'can', 'be', 'just', 'the', 'one', 'u', 'wanna', 'be'],
                       ['yo', 'ran', 'climb', 'sar'],
                       ['u', 'can', 'be', 'just-the-one', 'u-wanna-be'],
                       ['u u u u u u u u', 'ran', 'climb', 'sar  u u u u u u'],
                       ['let it go ~ let it go ~ !!!!'],
                       ['hello world']]

        for i in range(6):
            msg = self.commonsh.execut_db_sql(sql_list[i])
            logger.info(msg)
            result_lines = msg.splitlines()[2:-1]
            for line in result_lines:
                self.assertTrue(line.strip() == result_list[i][result_lines.index(line)])

    def tearDown(self):
        logger.info('--------------Opengauss_Function_Innerfunc_Regexp_Split_To_Table_Case0009执行结束-------------')
