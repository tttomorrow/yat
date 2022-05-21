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
Case Name   : 使用current_date函数获取当前日期
Description : current_date描述：当前日期。
    1.正常获取
    2.异常校验
Expect      :
    1.获取正确
    2.异常报错
History     :
"""

import unittest
import sys
import time
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("--Opengauss_Function_Innerfunc_Current_Date_Case0001开始--")
        self.commonsh = CommonSH('dbuser')

    def test_sysdate(self):
        current_time = time.strftime("%Y-%m-%d", time.localtime())
        # 正常获取
        cmd = '''select current_date;'''
        msg = self.commonsh.execut_db_sql(cmd)
        LOG.info(msg)
        db_time = msg.splitlines()[2].strip()
        self.assertTrue(db_time == current_time)
        # 错误调用
        cmd1 = '''select current_date();'''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        LOG.info(msg1)
        self.assertTrue('ERROR:  syntax error at or near "("' in msg1)

    def tearDown(self):
        LOG.info('--Opengauss_Function_Innerfunc_Current_Date_Case0001结束--')