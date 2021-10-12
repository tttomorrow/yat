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
Case Name   : 使用pg_systimestamp()函数获取系统时间戳.
Description : pg_systimestamp()描述：获取系统时间戳.返回值类型：timestamp with time zone
    1.正常获取select clock_timestamp();
    2.异常校验
Expect      :
    1.函数返回结果正确
    2.异常报错
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("Opengauss_Function_Innerfunc_Pg_Systimestamp_Case0001开始")
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_timestamp(self):
        now = self.user.sh('date "+%Y-%m-%d %H:%M:%S"').result()
        # 测试点1：正常获取
        cmd = '''select pg_systimestamp();'''
        msg = self.commonsh.execut_db_sql(cmd)
        LOG.info(msg)
        db_time = msg.splitlines()[2].strip()  # 2021-01-08 14:57:24.228786+08
        self.assertTrue(len(db_time) > 23)
        cmd2 = f"select '{now}'::timestamp - '{db_time}'::timestamp;"
        msg2 = self.commonsh.execut_db_sql(cmd2)
        LOG.info(msg2)
        diff = msg2.splitlines()[-2].strip().strip('-')
        self.assertTrue(diff[:5] == '00:00')
        self.assertTrue(db_time[-3:] == '+08')
        # 测试点2：错误调用
        cmd1 = '''select pg_systimestamp(2); select pg_systimestamp;'''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        LOG.info(msg1)
        self.assertTrue(msg1.count('ERROR') == 2)

    def tearDown(self):
        LOG.info("Opengauss_Function_Innerfunc_Pg_Systimestamp_Case0001结束")