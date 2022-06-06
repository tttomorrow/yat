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
Case Name   : 数字操作符>>(二进制右移)，右移位数为负数或浮点数
Description : 
    1. 右移位数给负数
    2. 右移位数给浮点数
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
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0005开始")
        self.commonsh = CommonSH('dbuser')

    def test_move(self):  # 右移位数为负数或浮点数
        move = {'-256': [-1, -1], '-32766.987': [14.11, -2],
                '8': [-2, 0], '262144': [-15.9, 4]}
        for i in range(len(move)):
            cmd = f"""select {list(move.keys())[i]} >> 
                            {list(move.values())[i][0]};"""
            msg1 = self.commonsh.execut_db_sql(cmd)
            LOG.info(msg1)
            result = msg1.splitlines()[2].strip()
            expect = str(list(move.values())[i][1])
            self.assertTrue(result == expect)

    def tearDown(self):
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0005结束")