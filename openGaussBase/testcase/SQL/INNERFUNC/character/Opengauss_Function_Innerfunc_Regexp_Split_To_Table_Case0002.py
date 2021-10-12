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
Case Name   : regexp_split_to_table函数对中文进行切割
Description : 用POSIX正则表达式作为分隔符，分隔string。
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.被分割字符串是中文
Expect      :
    步骤 1：数据库状态正常
    步骤 2：返回分割后结果text正确
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
        logger.info("------------Opengauss_Function_Innerfunc_Regexp_Split_To_Table_Case0002开始执行--------------")
        self.commonsh = CommonSH('dbuser')

    def test_function(self):
        logger.info("-------------•regexp_split_to_table函数对中文字符采用空格、字符串等进行分离---------------")

        cmd_pre = """   drop table if exists type_char;
                        create table type_char (string1 char(100));
                        insert into type_char values ('老师 好');
                        insert into type_char values ('好 老师');
                        insert into type_char values ('我 爱 你 祖 国');
                        insert into type_char values ('亲爱的             母亲');
                        insert into type_char values ('for our 民族之                  崛起         而奋斗！！！！！！');
                        insert into type_char values ('唱：why not president be a dreamer');"""
        self.commonsh.execut_db_sql(cmd_pre)

        cmd_check = """select * from type_char;"""
        msg1 = self.commonsh.execut_db_sql(cmd_check)
        logger.info(msg1)

        sql_list = [r"""select regexp_split_to_table(string1,E'\\\s+') from type_char;""",
                    r"""select regexp_split_to_table('你好  我好  大家好 ', E'好  ');""",
                    r"""select regexp_split_to_table('you!是she#是we$是they%是',E'是');"""]

        result_list = [['老师', '好', '好', '老师', '我', '爱', '你', '祖', '国', '亲爱的', '母亲',
                        'for', 'our', '民族之', '崛起', '而奋斗！！！！！！',
                        '唱：why', 'not', 'president', 'be', 'a', 'dreamer'],
                       ['你', '我', '大家好'],
                       ['you!', 'she#', 'we$', 'they%', '']]

        for i in range(3):
            msg = self.commonsh.execut_db_sql(sql_list[i])
            logger.info(msg)
            result_lines = msg.splitlines()[2:-1]
            for line in result_lines:
                self.assertTrue(line.strip() == result_list[i][result_lines.index(line)])

        self.commonsh.execut_db_sql("""drop table if exists type_char;""")

    def tearDown(self):
        logger.info('--------------Opengauss_Function_Innerfunc_Regexp_Split_To_Table_Case0002执行结束-------------')
