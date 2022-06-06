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
Case Name   : 使用to_char函数将sysdate的年份以指定格式输出
Description : sysdate描述：当前日期及时间。返回值类型：timestamp
    1.执行语句SELECT TO_CHAR(SYSDATE,text);
    text为对年份的指定格式
Expect      :
    1.返回正确
"""

import unittest
import time
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("--Opengauss_Function_Innerfunc_Sysdate_Case0003开始--")
        self.commonsh = CommonSH('dbuser')

    def test_sysdate(self):
        text = {'IYYY': 'ISO标准4位数字年',
                'Y,YYY': '带逗号的年(4和更多位)',
                'YYYY': '年(4和更多位)',
                'YYY,YY,Y': '年的后三位、年的后两位、年的最后一位'}
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.log.info('当前时间是：' + now)
        year = now.split('-')[0]
        exp = [year,
               year[:-3] + ',' + year[-3:],
               year,
               year[-3:] + ',' + year[-2:] + ',' + year[-1]]
        self.log.info(f'期望的年份输出是：\n{exp}')
        for i in range(4):
            self.log.info("----------执行SQL语句：----------")
            cmd = f"select sysdate,to_char(sysdate,'{list(text.keys())[i]}');"
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            res = msg.split('\n')[2].split('|')[1].strip()
            flag = False  
            if res == exp[i]:
                self.log.info('结果与期望的值相等')
                flag = True
            else:
                res_time = msg.split('\n')[2].split('|')[0].strip()
                cmd1 = f"select '{now}'::timestamp - '{res_time}'::timestamp;"
                msg1 = self.commonsh.execut_db_sql(cmd1)
                self.log.info(msg1)
                diff = msg1.splitlines()[-2].strip().lstrip('-')
                self.assertTrue(diff[:5] <= '00:05')
                self.log.info('实际结果与期望之间跨年，差异不超过五分钟')
                flag = True
            self.assertTrue(flag)

    def tearDown(self):
        self.log.info("--Opengauss_Function_Innerfunc_Sysdate_Case0003结束--")