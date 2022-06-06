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
Case Name   : Jsonb额外支持的操作符:?&数组字符串中的所有是否做为顶层键存在,右侧操作数为text[]
Description :
    1.数组字符串中的所有做为顶层键存在
    2.数组字符串中的所有做为顶层键不存在
Expect      :
    1.数组字符串中的所有做为顶层键存在,执行结果为t
    2.数组字符串中的所有做为顶层键不存在,执行结果为f
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
        self.log.info('---Opengauss_Function_Datatype_Jsonb_Case0039开始---')
        self.log.info('------数组字符串中的所有做为顶层键存在,执行结果为t------')
        sql_cmd1 = r'''
            select '\"str\"'::jsonb ?& array['str'];
            select '\"null\"'::jsonb ?& array['null'];
            select '{{\"a\":1, \"b\": [1,2,3],\"c\":{{\"b\":\"d\"}}}}'
            ::jsonb ?& array['a','b','c'];
            select '{{\"a\":1,\"b\": [1,2,3],\"c\":{{\"b\":\"d\"}}}}'
            ::jsonb ?& array['b','c'];
            select '[null, false,\"123\",{{\"a\":true}},\"test\"]'
            ::jsonb ?& array['test','123'];
            '''
        self.log.info(sql_cmd1)
        msg1 = self.dbuser.execut_db_sql(sql_cmd1)
        self.log.info(msg1)
        self.assertEqual(5, msg1.count('t\n'))
        self.assertEqual(5, msg1.count('1 row'))

        self.log.info('------数组字符串中的所有做为顶层键不存在,执行结果为f------')
        sql_cmd2 = r'''
            select 'null'::jsonb ?& array['null'];
            select 'false'::jsonb ?& array['false'];
            select 'true'::jsonb ?& array['true'];
            select '{{\"a\":1, \"b\": [1,2,3],\"c\":{{\"b\":\"d\"}}}}'
            ::jsonb ?& array['c','d'];
            select '[null, false, 123,{{\"a\":true}},\"test\"]'
            ::jsonb ?& array['123','a'];
            select '[null, false, 123,{{\"a\":true}},\"test\"]'
            ::jsonb ?& array['{{\"a\":true}}'];
            select '105.2e3'::jsonb ?& array['105200'];
            select '[{{\"a\":true}}, null] ':: jsonb ?& array['b','null'];
            '''
        msg2 = self.dbuser.execut_db_sql(sql_cmd2)
        self.log.info(msg2)
        self.assertEqual(8, msg2.count('f\n'))
        self.assertEqual(8, msg2.count('1 row'))

    def tearDown(self):
        self.log.info('------------------无需清理环境-----------------')
        self.log.info('---Opengauss_Function_Datatype_Jsonb_Case0039结束---')
