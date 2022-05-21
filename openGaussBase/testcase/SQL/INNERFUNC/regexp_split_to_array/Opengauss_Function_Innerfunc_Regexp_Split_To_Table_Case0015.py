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
Case Name   : regexp_split_to_array函数对可选参数flag的验证
Description : regexp_split_to_table(string text, pattern text [, flags text])用POSIX正则表达式作为分隔符，分隔string。
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.入参是特殊字符
Expect      :
    步骤 1：数据库状态正常
    步骤 2：返回分割后结果text[]正确
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
        logger.info("------------Opengauss_Function_Innerfunc_Regexp_Split_To_Table_Case0015开始执行--------------")
        self.commonsh = CommonSH('dbuser')

    def test_function(self):
        logger.info("-------------regexp_split_to_table函数可选参数的验证--------------")
        #  i表示大小敏感，c表示大小写不敏感，一起使用以最后一个为准
        sql_list = [r"""SELECT regexp_split_to_table('Yes no yes NO YES No yES', 'NO','c');""",
                    r"""SELECT regexp_split_to_table('Yes no yes NO YES No yES', 'NO','i');""",
                    r"""SELECT regexp_split_to_table('Yes no yes NO YES No yES', 'no','c');""",
                    r"""SELECT regexp_split_to_table('Yes no yes NO YES No yES', 'no','i');""",
                    r"""SELECT regexp_split_to_table('Yes no yes NO YES No yES', 'nO','c');""",
                    r"""SELECT regexp_split_to_table('Yes no yes NO YES No yES', 'nO','i');""",
                    r"""SELECT regexp_split_to_table('Yes no yes NO YES No yES', 'No','c');""",
                    r"""SELECT regexp_split_to_table('Yes no yes NO YES No yES', 'No','i');""",
                    r"""SELECT regexp_split_to_table('yes no yes NO yes No yes', 'NO','ccci');""",
                    r"""SELECT regexp_split_to_table('yes no yes NO yes No yes', 'NO','mc');"""]

        result_list = [['Yes no yes', 'YES No yES'],
                       ['Yes', 'yes', 'YES', 'yES'],
                       ['Yes', 'yes NO YES No yES'],
                       ['Yes', 'yes', 'YES', 'yES'],
                       ['Yes no yes NO YES No yES'],
                       ['Yes', 'yes', 'YES', 'yES'],
                       ['Yes no yes NO YES', 'yES'],
                       ['Yes', 'yes', 'YES', 'yES'],
                       ['yes', 'yes', 'yes', 'yes'],
                       ['yes no yes', 'yes No yes']]

        for i in range(10):
            msg = self.commonsh.execut_db_sql(sql_list[i])
            logger.info(msg)
            result_lines = msg.splitlines()[2:-1]
            for line in result_lines:
                self.assertTrue(line.strip() == result_list[i][result_lines.index(line)])

    def tearDown(self):
        logger.info('--------------Opengauss_Function_Innerfunc_Regexp_Split_To_Table_Case0015执行结束-------------')
