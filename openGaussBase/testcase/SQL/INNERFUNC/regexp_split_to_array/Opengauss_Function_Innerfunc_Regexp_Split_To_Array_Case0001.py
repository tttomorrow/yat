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
Case Name   : regexp_split_to_array函数采用空格、字符串等对string进行分离
Description : 用POSIX正则表达式作为分隔符，分隔string。
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
        logger.info("------------Opengauss_Function_Innerfunc_Regexp_Split_To_Array_Case0001开始执行--------------")
        self.commonsh = CommonSH('dbuser')

    def test_function(self):
        logger.info("-------------•regexp_split_to_array函数采用空格、字符串等进行分离---------------")

        sql_list = [r"""SELECT regexp_split_to_array('hello world', E'\\\s+');""",
                    r"""SELECT regexp_split_to_array('321            new    world', E'\\\s+');""",
                    r"""SELECT regexp_split_to_array('power     your   world', E'\\\s+');""",
                    r"""SELECT regexp_split_to_array('please   hello   world', E'hello');"""]

        result_list = ['{hello,world}', '{321,new,world}', '{power,your,world}', '{"please   ","   world"}']
        for i in range(4):
            msg = self.commonsh.execut_db_sql(sql_list[i])
            logger.info(msg)
            self.assertTrue(msg.splitlines()[2].strip() == result_list[i])

    def tearDown(self):
        logger.info('--------------Opengauss_Function_Innerfunc_Regexp_Split_To_Array_Case0001执行结束-------------')
