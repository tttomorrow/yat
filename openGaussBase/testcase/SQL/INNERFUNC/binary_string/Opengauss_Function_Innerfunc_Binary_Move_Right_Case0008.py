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
Case Name   : 数字操作符>>(二进制右移)，空值及缺少参数的校验
Description :
    1. 移动位数是空值、空值进行右移
    2. 参数缺少
Expect      :
    1. 返回空
    2. 提示操作符使用有误
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0007开始")
        self.commonsh = CommonSH('dbuser')

    def test_right1(self):
        cmd = ["select null >> 2;", "select 8 >> null;",
               "select '' >> 2;", "select 8 >> '';"]
        for i in range(4):
            msg = self.commonsh.execut_db_sql(cmd[i])
            LOG.info(msg)
            self.assertTrue(msg.splitlines()[2].strip() == '')

    def test_right2(self):
        cmd = "select 8 >>; select >> 2;"
        msg = self.commonsh.execut_db_sql(cmd)
        LOG.info(msg)
        self.assertTrue(msg.count('ERROR') == 2)

    def tearDown(self):
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0007结束")