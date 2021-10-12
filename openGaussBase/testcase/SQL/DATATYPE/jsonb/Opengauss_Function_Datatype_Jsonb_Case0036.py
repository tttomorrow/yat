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
Case Name   : Jsonb额外支持的操作符:? 键/元素字符串是否存在于 JSON 值的顶层，右侧操作数为非text，合理报错
Description :
    1.键/元素字符串是否存在于 JSON 值的顶层,右侧操作数为非text，合理报错
    2.包含隐式转化的数据类型
Expect      :
    1.键/元素字符串存在于 JSON 值的顶层,右侧操作数为非text，合理报错
    2.隐式转化成功，sql语句有正常的执行结果
History     :
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Jsonb(unittest.TestCase):

    def setUp(self):
        self.constant = Constant()
        self.dbuser = CommonSH('dbuser')
        self.log = Logger()

    def test_copy(self):
        self.log.info('---Opengauss_Function_Datatype_Jsonb_Case0036开始---')
        self.log.info('------键/元素字符串是否存在于 JSON 值的顶层,右侧操作数为非text，合理报错------')
        sql_cmd1 = r'''
        select '{{\"a\":1, \"b\":2}}'::jsonb ? (select '\"b\"'::jsonb);
            select '{{\"a\":1, \"b\":2}}'::jsonb ? (select '\"b\"'::jsonb);
            select '[\"abcdefg\",1,{{\"db\":\"test\"}},null,\"true\",false]'::
            jsonb ? (select 'true'::jsonb);
            select '[\"abcdefg\",138,{{\"db\":\"test\"}},null,\"true\",
            false]'::jsonb ? abcdefg;
            select '[\"abcdefg\",138,\"{{\\\"db\\\":\\\"test\\\"}}\",null,
            \"true\",false]'::jsonb ? \"db\";
            select '[\"abcdefg\",\"138\",{{\"db\":\"test\"}},\"null\",
            \"true\",false]'::jsonb ?  (select 'true'::int);
            '''
        self.log.info(sql_cmd1)
        msg1 = self.dbuser.execut_db_sql(sql_cmd1)
        self.log.info(msg1)
        self.assertEqual(6, msg1.count('ERROR:'))

        self.log.info('--------隐式转化成功，sql语句有正常的执行结果---------')
        sql_cmd2 = r'''
            select '[\"abcdefg\",1,{{\"db\":\"test\"}},null,\"true\",
            false]'::jsonb ? (select true ::int);
            select '[\"abcdefg\",138.66,{{\"db\":\"test\"}},null,\"true\",
            false]'::jsonb ? 138.66;
            select '158'::jsonb ? 158;
            select 'false'::jsonb ? (select false ::int);
            select 'true'::jsonb ? (select true ::int);
            '''
        msg2 = self.dbuser.execut_db_sql(sql_cmd2)
        self.log.info(msg2)
        self.assertEqual(5, msg2.count('f\n'))
        self.assertEqual(5, msg2.count('1 row'))


    def tearDown(self):
        self.log.info('--无需清理环境--')
        self.log.info('---Opengauss_Function_Datatype_Jsonb_Case0036结束---')