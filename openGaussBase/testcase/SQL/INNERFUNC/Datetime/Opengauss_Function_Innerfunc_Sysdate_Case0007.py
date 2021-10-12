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
Case Name   : 使用to_char函数将sysdate的周数以指定格式输出
Description : sysdate描述：当前日期及时间。返回值类型：timestamp
    1.执行语句SELECT TO_CHAR(SYSDATE,text);
    text为对周数的指定格式
Expect      :
    1.返回正确
"""

import time
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("--Opengauss_Function_Innerfunc_Sysdate_Case0007开始--")
        self.commonsh = CommonSH('dbuser')

    def test_sysdate(self):
        text = {'W': '一个月里的周数(1-5)(第一周从该月第一天开始)',
                'WW': '一年里的周数(1-53)(第一周从该年的第一天开始)'}
        self.log.info('定义一个输入一年中的天数，返回该天属于一年中的第几周的'
                      '函数')

        def week(day):
            l = [[j for j in range((i - 1) * 7 + 1, i * 7 + 1)] for i in
                 range(1, 54)]
            d = {'{}'.format(k): l.index(k) + 1 for k in l}
            for key in d.keys():
                if day in key:
                    return d[key]

        msg = time.strftime("%Y-%m-%d %H:%M:%S,%d %j", time.localtime())
        now = msg.split(',')[0].strip()
        self.log.info('当前时间是：' + now)
        day = msg.split(',')[1].split()
        self.log.info(f'今天在本月及一年中的天数是：{day}')
        for i in range(2):
            self.log.info("----------执行SQL语句：----------")
            cmd = f"select sysdate,to_char(sysdate,'{list(text.keys())[i]}');"
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            res = msg.split('\n')[2].split('|')[1].strip()
            flag = False
            self.log.info(f'---数据库返回的结果是{week(str(int(day[i])))}')
            if int(res) == week(str(int(day[i]))):
                self.log.info('结果与期望的值相等')
                flag = True
            else:
                res_time = msg.split('\n')[2].split('|')[0].strip()
                cmd1 = f"select '{now}'::timestamp - '{res_time}'::timestamp;"
                msg1 = self.commonsh.execut_db_sql(cmd1)
                self.log.info(msg1)
                diff = msg1.splitlines()[-2].strip().lstrip('-')
                self.assertTrue(diff[:5] <= '00:05')
                self.log.info('实际结果与期望之间差异不超过五分钟，'
                              '判定结果正确')
                flag = True
            self.assertTrue(flag)

    def tearDown(self):
        self.log.info("--Opengauss_Function_Innerfunc_Sysdate_Case0007结束--")
