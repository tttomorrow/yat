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
Case Name   : now函数与distinct和union all联合使用
Description : now()描述：当前日期及时间。
    1.与current_timestamp函数交替执行结果进行union all后distinct
Expect      :
    1.返回三行时间日期信息
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("--Opengauss_Function_Innerfunc_Now_Case0004开始--")
        self.commonsh = CommonSH('dbuser')

    def test_now(self):
        cmd = '''select distinct * from (
            select now()
            union all
            select current_timestamp(2)
            union
            select now() 
            union all
            select current_timestamp
            union all
            select now()
            union all
            select current_timestamp(2));'''
        msg = self.commonsh.execut_db_sql(cmd)
        LOG.info(msg)
        res = msg.splitlines()[2:5]
        self.assertTrue('(3 rows)' in msg)
        self.assertTrue(len(set(list(map(lambda s: s[:20], res)))) == 1)

    def tearDown(self):
        LOG.info('--Opengauss_Function_Innerfunc_Now_Case0004结束--')