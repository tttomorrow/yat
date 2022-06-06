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
Case Name   : sysdate与to_char、to_date函数交互使用
Description : sysdate描述：当前日期及时间。返回值类型：timestamp
    1.sysdate作为to_char、to_date的入参，将结果进行转换
Expect      :
    1.返回正确
"""

import unittest
import time
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("--Opengauss_Function_Innerfunc_Sysdate_Case0002开始--")
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_sysdate(self):

        cmd = ["select sysdate;",
               "select to_date(to_char(sysdate,'YYYY-MM-DD'), 'yyyy-MM-dd');",
               "select to_date(sysdate, 'yyyy-MM-dd HH24:mi:ss');"]

        for i in range(1, 3):
            msg0 = self.commonsh.execut_db_sql(cmd[0])
            self.log.info(msg0)
            boundary = msg0.split('\n')[2].strip()
            if boundary.split()[1] == '23:59:59':
                time.sleep(1)
            self.log.info("=========现在的时间的是：==========")
            msg1 = self.user.sh('date "+%Y-%m-%d %H:%M:%S"').result()
            self.log.info(msg1)
            now = msg1.strip()

            self.log.info("=========执行SQL语句：==========")
            msg2 = self.commonsh.execut_db_sql(cmd[i])
            self.log.info(msg2)
            res = msg2.split('\n')[2].strip()
            self.assertTrue(len(res) == 19)
            if i == 1:
                self.assertTrue(res == now.split()[0] + ' 00:00:00')
            else:
                self.log.info("===判断执行结果与当前时间差值不超过五分钟===")
                cmd3 = f"select '{now}'::timestamp - '{res}'::timestamp;"
                msg3 = self.commonsh.execut_db_sql(cmd3)
                self.log.info(msg3)
                diff = msg3.splitlines()[-2].strip().lstrip('-')
                self.assertTrue(diff[:5] <= '00:05')

    def tearDown(self):
        self.log.info("--Opengauss_Function_Innerfunc_Sysdate_Case0002结束--")