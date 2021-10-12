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
Case Name   : 数字操作符>>(二进制右移)，0右移或者右移0位
Description :
    1.  给值是0的列右移，给某列右移0位
    2. 正负数进行右移0位，给0进行右移
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
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0004开始")
        self.commonsh = CommonSH('dbuser')

    def test_move_right1(self):
        cmd = '''drop table if exists test;
        create table test(c1 float, c2 integer);
        insert into test values(0,-1024);
        msg = self.commonsh.execut_db_sql(cmd)
        LOG.info(msg)
        cmd1 = "select c1 >> 2, c2 >> 0 from test;"
        msg0 = self.commonsh.execut_db_sql(cmd1)
        LOG.info(msg0)
        line1 = '''0 |      -1024'''
        self.assertTrue(msg0.splitlines()[-3].strip() == line1)
        self.assertTrue(msg0.splitlines()[-2].strip() == line2)

    def test_move_right2(self):
        move = {'-256': [0, -256], '-32767.9': [0, -32768],
                '8': [0, 8], '0.0': [12, 0], '0': [14, 0]}
        for i in range(len(move)):
            cmd = f"""select {list(move.keys())[i]} >> 
                            {list(move.values())[i][0]};"""
            msg1 = self.commonsh.execut_db_sql(cmd)
            LOG.info(msg1)
            expect = str(list(move.values())[i][1])
            result = msg1.splitlines()[2].strip()
            self.assertTrue(expect == result)

    def tearDown(self):
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0004结束")