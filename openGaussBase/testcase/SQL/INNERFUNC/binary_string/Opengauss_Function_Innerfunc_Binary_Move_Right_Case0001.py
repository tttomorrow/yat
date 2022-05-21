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
Case Name   : 数字操作符>>(二进制右移)，对移动规则的校验
Description : 假设 x=2^a，右移位数 y
    1. 右移位数y在（0-a）内
    2. 右移位数y<0、y>a
Expect      :
    1. 返回结果是x除以2的右移位数次方
    2. 返回-1、0、如果移动的位数超过了该类型的最大位数，那么编译器会对移动的位数取模。
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0001开始")
        self.commonsh = CommonSH('dbuser')

    def test_move(self):
        bit_num = [-59, -18, -5, -2, 0, 5, 15, 35, 86]
        result = [[-1024, -2, -1, -1, -32768, -1024, -1, -4096, -1],
                  [1023, 1, 0, 0, 32767, 1023, 0, 4095, 0]]
        for i in range(9):
            cmd = f'''select -32768 >> {bit_num[i]};
                       select 32767 >> {bit_num[i]};'''
            LOG.info(cmd)
            msg = self.commonsh.execut_db_sql(cmd)
            LOG.info(msg)
            res1 = int(msg.splitlines()[2].strip())
            res2 = int(msg.splitlines()[-2].strip())
            self.assertTrue(res1 == result[0][i])
            self.assertTrue(res2 == result[1][i])

    def tearDown(self):
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0001结束")
