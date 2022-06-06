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
Case Name   : 使用sysdate函数获取当前日期及时间
Description : sysdate描述：当前日期及时间。返回值类型：timestamp
    1.正常获取
    2.异常校验
Expect      :
    1.获取正确
    2.异常报错
History     :
"""

import unittest
import time
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('''--------
            Opengauss_Function_Innerfunc_Sysdate_Case0001开始--------''')
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_sysdate(self):
        msg = self.user.sh('date "+%Y-%m-%d %H:%M:%S"').result()
        self.log.info(msg)
        current_time = msg.strip()
        # 测试点1：正常获取
        cmd1 = '''select sysdate;'''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        db_time = msg1.splitlines()[2].strip()  # 2021-01-08 14:43:14.005565+8
        cmd2 = f"select '{current_time}'::timestamp - '{db_time}'::timestamp;"
        msg2 = self.commonsh.execut_db_sql(cmd2)
        self.log.info(msg2)
        diff = msg2.splitlines()[-2].strip()
        self.assertTrue(diff.split(':')[1] == '00')
        # 错误调用
        cmd1 = '''select sysdate();'''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue('ERROR:  syntax error at or near "("' in msg1)

    def tearDown(self):
        self.log.info('''--------
            Opengauss_Function_Innerfunc_Sysdate_Case0001结束--------''')
