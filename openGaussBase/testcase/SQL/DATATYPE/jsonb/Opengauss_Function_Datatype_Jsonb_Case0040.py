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
Case Name   : Jsonb额外支持的操作符:?&数组字符串中的任何一个是否做为顶层键存在,右侧操作数为非text[]
Description :
    数组字符串中的任何一个是否做为顶层键存在,右侧操作数为非text[]
Expect      :
    右侧操作数为非text[],不符合操作符入参要求，结果合理报错
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
        self.log.info('---Opengauss_Function_Datatype_Jsonb_Case0040开始---')
        self.log.info('------右侧操作数为非text[],不符合操作符入参要求，结果合理报错------')
        sql_cmd1 = r'''
            select '\"str\"'::jsonb ?&  'str';
            select '\"null\"'::jsonb ?& 'null';
            select 'false'::jsonb ?& 'false';
            select 'true'::jsonb ?& 'true';
            select '{{\"a\":1,\"b\": [10,2,3],\"c\":{{\"b\":\"d\"}}}}'
            ::jsonb ?& (select 'b'::jsonb);
            select '{{\"a\":1,\"b\": [1,2,3],\"c\":{{\"b\":\"d\"}}}}'
            ::jsonb ?& '{{'b','d'}}';
            select '[null, false, 123,{{\"a\":true}},\"test\"]'
            ::jsonb ?& '[123,'{{a}}']';
            select '[null, false, 123,{{\"a\":true}},\"test\"]'
            ::jsonb ?& array['test',123];
            select '[{{\"a\":true}}, null] ':: jsonb ?& 'b';
            select '105.2e3'::jsonb ?& '105200';
            '''
        self.log.info(sql_cmd1)
        msg1 = self.dbuser.execut_db_sql(sql_cmd1)
        self.log.info(msg1)
        self.assertEqual(10, msg1.count('ERROR:'))

    def tearDown(self):
        self.log.info('------------------无需清理环境-----------------')
        self.log.info('---Opengauss_Function_Datatype_Jsonb_Case0040结束---')