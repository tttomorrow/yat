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
Case Name   : 数字操作符>>(二进制右移)，正负浮点型数值右移
Description :
    1. 对正负浮点型数值的列进行二进制右移
    2. 对整数浮点型数数值进行二进制右移
Expect      :
    1. 返回结果正确
    2. 返回结果正确
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0003开始")
        self.commonsh = CommonSH('dbuser')

    def test_move_right1(self):
        cmd = '''drop table if exists test;
        create table test(c1 float4, c2 float(3), c3 decimal(10,4));
        insert into test values(10.365456,10.3214,123.123654);
        insert into test values(-10.365456,-10.3214,-123.123654);'''
        msg = self.commonsh.execut_db_sql(cmd)
        LOG.info(msg)
        cmd1 = "select c1 >> 2, c2 >> 3, c3 >> 5 from test;"
        msg0 = self.commonsh.execut_db_sql(cmd1)
        LOG.info(msg0)
        line1 = '''2 |        1 |        3'''
        line2 = '''-3 |       -2 |       -4'''
        self.assertTrue(msg0.splitlines()[-3].strip() == line1)
        self.assertTrue(msg0.splitlines()[-2].strip() == line2)

    def test_move_right2(self):
        move = {'-256.01': [1, -128], '-32767.29': [14, -2],
                '7.51': [2, 2], '32767.87': [12, 8], '262143.999': [14, 16]}
        for i in range(len(move)):
            cmd = f"""select {list(move.keys())[i]} >> 
                            {list(move.values())[i][0]};"""
            msg1 = self.commonsh.execut_db_sql(cmd)
            LOG.info(msg1)
            expect = str(list(move.values())[i][1])
            result = msg1.splitlines()[-2].strip()
            self.assertTrue(result == expect)

    def tearDown(self):
        self.commonsh.execut_db_sql('drop table if exists test cascade;')
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0003结束")