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
Case Name   : 使用clock_timestamp()函数返回实时时钟的当前时间戳
Description : clock_timestamp()描述：实时时钟的当前时间戳。
    1.正常获取select clock_timestamp();
    2.异常校验
Expect      :
    1.函数返回结果正确
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
            Opengauss_Function_Innerfunc_Clock_Timestamp_Case0001开始----''')
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_time(self):
        msg = self.user.sh('date "+%Y-%m-%d %H:%M:%S"').result()
        self.log.info(msg)
        current_time = msg.strip()
        # 测试点1：正常获取
        cmd1 = '''select clock_timestamp();'''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        db_time = msg1.splitlines()[2].strip()  # 2021-01-08 14:43:14.005565+8
        cmd2 = f"select '{current_time}'::timestamp - '{db_time}'::timestamp;"
        msg2 = self.commonsh.execut_db_sql(cmd2)
        self.log.info(msg2)
        diff = msg2.splitlines()[-2].strip()
        self.assertTrue(diff.split(':')[1] == '00')
        # 测试点2：错误调用
        cmd3 = '''select clock_timestamp; 
            select clock_timestamp(now);
            '''
        msg3 = self.commonsh.execut_db_sql(cmd3)
        self.log.info(msg3)
        self.assertTrue(msg3.count('ERROR') == 2)

    def tearDown(self):
        self.log.info('''--------
            Opengauss_Function_Innerfunc_Clock_Timestamp_Case0001执行结束---''')
