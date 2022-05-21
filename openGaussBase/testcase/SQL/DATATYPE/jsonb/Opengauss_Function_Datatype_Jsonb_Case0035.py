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
Case Name   : Jsonb额外支持的操作符:? 键/元素字符串是否存在于 JSON 值的顶层，右侧操作数为text
Description :
    1.键/元素字符串是否存在于 JSON 值的顶层
    2.键/元素字符串是否不存在于 JSON 值的顶层
    3.其他格式：null_json,bool_json,unm_json
Expect      :
    1.键/元素字符串存在于 JSON 值的顶层
    2.键/元素字符串不存在于 JSON 值的顶层
    3.其他格式：null_jsonb,bool_jsonb,num_jsonb
History     :
"""

import os
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
        self.log.info('---Opengauss_Function_Datatype_Jsonb_Case0035开始---')
        self.log.info('---------键/元素字符串存在于 JSON 值的顶层---------')
        sql_cmd1 = r'''
            select '\"188\"'::jsonb ? 188;
            select '\"188\"'::jsonb ? '188';
            select '{{\"a\":1, \"b\":2}}'::jsonb ? 'b';
            select '[\"abcdefg\",1,{{\"db\":\"test\"}},null,\"true\",false]'
            ::jsonb ? 'true';
            select '[\"abcdefg\",138,{{\"db\":\"test\"}},null,\"true\",false]'
            ::jsonb ? 'abcdefg';
            select '[\"abcdefg\",\"138\",{{\"db\":\"test\"}},\"null\",
            \"true\",false]'::jsonb ? 'null';
            select '[\"abcdefg\",138,\"{{\\\"db\\\":\\\"test\\\"}}\",null,
            \"true\",false]'::jsonb ? '{{\"db\":\"test\"}}';
            select '[\"abcdefg\",1,{{\"db\":\"test\"}},null,\"true\",false]'
            ::jsonb ? (select true ::text);
            select '[\"abcdefg\",138,\"{{\\\"db\\\":\\\"test\\\"}}\",null,
            \"true\",false]'::jsonb ? '{{\"db\":\"test\"}}';'''
        msg1 = self.dbuser.execut_db_sql(sql_cmd1)
        self.log.info(msg1)
        self.assertEqual(9, msg1.count('t\n'))
        self.assertEqual(9, msg1.count('1 row'))

        self.log.info('---------键/元素字符串不存在于 JSON 值的顶层---------')
        sql_cmd2 = r'''
            select '\"188\"'::jsonb ? '\"188\"';
            select '{{\"a\":1, \"b\":2}}'::jsonb ? '\"b\"';
            select '[\"abcdefg\",1,{{\"db\":\"test\"}},null,\"true\",false]'
            ::jsonb ? ' ';
            select '[\"abcdefg\",138,{{\"db\":\"test\"}},null,\"true\",false]'
            ::jsonb ? (select 138 ::text);
            select '[\"abcdefg\",\"138\",{{\"db\":\"test\"}},\"null\",
            \"true\",false]'::jsonb ?  '{{\"db\":\"test\"}}';
            select '[\"abcdefg\",1,{{\"db\":\"test\"}},null,\"true\",false]'
            ::jsonb ? (select false ::text);'''
        msg2 = self.dbuser.execut_db_sql(sql_cmd2)
        self.log.info(msg2)
        self.assertEqual(6, msg2.count('f\n'))
        self.assertEqual(6, msg2.count('1 row'))

        self.log.info('----------null_jsonb,bool_jsonb,num_jsonb-------')
        sql_cmd3 = r'''
            select '158'::jsonb ? '158';
            select null::jsonb ? 'null';
            select 'true'::jsonb ? 'true';
            '''
        msg3 = self.dbuser.execut_db_sql(sql_cmd3)
        self.log.info(msg3)
        self.assertEqual(3, msg3.count('1 row'))
        self.assertEqual(2, msg3.count('f\n'))


    def tearDown(self):
        self.log.info('--无需清理环境--')