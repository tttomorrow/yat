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
Case Name   : add_months函数边界值校验
Description : add_months(d,n)描述：用于计算时间点d再加上n个月的时间。
    1. 参数2给边界值3531312
    2. 参数2给超过边界值3531313
Expect      : 
    1. 正常转换
    2. 提示报错
History     : 
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("Opengauss_Function_Innerfunc_Add_Months_Case0015开始")
        self.commonsh = CommonSH('dbuser')

    def test_add(self):  # 结果不能超过294277-01-09

        sql_cmd = """select add_months('294277-01-09','0');
                     select add_months('0001-01-01','3531313');
                     select add_months('294277-01-09','1');"""
        msg1 = self.commonsh.execut_db_sql(sql_cmd)
        LOG.info(msg1)
        res = '294277-01-09 00:00:00'
        self.assertTrue(msg1.splitlines()[2].strip() == res)
        flag = msg1.count('ERROR:  timestamp out of range') == 2
        self.assertTrue(flag)

    def tearDown(self):
        LOG.info("Opengauss_Function_Innerfunc_Add_Months_Case0015结束")