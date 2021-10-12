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
Case Name   : 使用localtime函数返回当前时间
Description : localtime描述：当前时间。
    1.正常获取select localtime;
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
        LOG.info("Opengauss_Function_Innerfunc_Localtime_Case0001开始")
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_time(self):
        now = self.user.sh('date "+%H:%M:%S"').result()
        # 测试点1：正常获取
        cmd = '''select localtime;'''
        msg = self.commonsh.execut_db_sql(cmd)
        LOG.info(msg)
        db_time = msg.splitlines()[2].strip()  # 14:37:52.993025
        self.assertTrue(len(db_time) > 9 and '.' in db_time)  # 带秒域
        cmd2 = f"select '{db_time}'::interval - '{now}'::interval;"
        msg2 = self.commonsh.execut_db_sql(cmd2)
        LOG.info(msg2)
        diff = msg2.splitlines()[-2].split()[-1].strip().strip('-')
        self.assertTrue(diff[:5] == '00:00')
        self.assertTrue('+08' not in db_time)
        # 测试点2：错误调用
        cmd1 = 'select localtime(); select localtime(+08);'
        msg1 = self.commonsh.execut_db_sql(cmd1)
        LOG.info(msg1)
        self.assertTrue(msg1.count('ERROR') == 2)

    def tearDown(self):
        LOG.info("Opengauss_Function_Innerfunc_Localtime_Case0001结束")