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
Case Name   : 使用to_char函数将sysdate的月份以指定格式输出
Description : sysdate描述：当前日期及时间。返回值类型：timestamp
    1.执行语句SELECT TO_CHAR(SYSDATE,text);
    text为对月份的指定格式
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
        self.log.info("--Opengauss_Function_Innerfunc_Sysdate_Case0004开始--")
        self.commonsh = CommonSH('dbuser')

    def test_sysdate(self):
        text = {'MONTH': '全长大写月份名(空白填充为9字符)',
             'Month': '全长混合大小写月份名(空白填充为9字符)',
             'month': '全长小写月份名(空白填充为9字符)',
             'MON': '大写缩写月份名(3字符)',
             'Mon': '缩写混合大小写月份名(3字符)',
             'mon': '小写缩写月份名(3字符)',
             'MM': '月份号(01-12)'}

        msg = time.strftime("%Y-%m-%d %H:%M:%S,%B %b %m", time.localtime())
        now = msg.split(',')[0].strip()
        self.log.info('当前时间是：' + now)
        month = msg.split(',')[1].split()
        exp = [month[0].upper(),
               month[0].capitalize(),
               month[0].lower(),
               month[1].upper(),
               month[1].capitalize(),
               month[1].lower(),
               month[2]]
        self.log.info(f'期望的月份输出是：\n{exp}')
        for i in range(7):
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
                self.log.info('实际结果与期望之间差异不超过五分钟，'
                              '判断结果正确')
                flag = True
            self.assertTrue(flag)

    def tearDown(self):
        self.log.info("--Opengauss_Function_Innerfunc_Sysdate_Case0004结束--")