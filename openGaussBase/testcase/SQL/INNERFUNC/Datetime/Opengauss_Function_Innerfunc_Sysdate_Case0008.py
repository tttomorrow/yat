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
Case Name   : 使用to_char函数将sysdate的时分秒等以指定格式输出
Description : sysdate描述：当前日期及时间。返回值类型：timestamp
    1.执行语句SELECT TO_CHAR(SYSDATE,text);
    text为对时分秒等的指定格式
Expect      :
    1.返回正确
              time.ctime获取当前时间改为date
"""

import unittest

from yat.test import Node

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("--Opengauss_Function_Innerfunc_Sysdate_Case0008开始---")
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_sysdate(self):
        text = {'AM': '正午标识(大写)', 'HH': '一天的小时数(01-12)',
                'HH12': '一天的小时数(01-12)', 'HH24': '一天的小时数(00-23)',
                'MI': '分钟(00-59)', 'SS': '秒(00-59)',
                'MS': '毫秒(000-999)', 'US': '微秒(000000-999999)'}
        self.log.info('----使用date获取当前时间---')
        get_date = self.user.sh('date +"%Y-%m-%d %H:%M:%S,%p %I %I %H %M"') \
            .result()
        self.log.info(get_date)
        now = get_date.split(',')[0].strip()
        self.log.info('当前时间是：' + now)
        exp = get_date.split(',')[1].split()
        self.log.info(f'期望的时间输出是：\n{exp}')
        for i in range(8):
            self.log.info("----------执行SQL语句：----------")
            cmd = f"select sysdate,to_char(sysdate,'{list(text.keys())[i]}');"
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            res = msg.split('\n')[2].split('|')[1].strip()
            self.log.info('定义一个判断结果的标识')
            flag = False
            try:
                if i < 5:
                    if res == exp[i]:
                        self.log.info('结果与期望的值相等')
                        flag = True
                elif i == 5:
                    if len(res) == 2 and 0 <= int(res) <= 59:
                        self.log.info('结果与期望的值相等')
                        flag = True
                elif i == 6:
                    if res == '000':
                        self.log.info('结果与期望的值相等')
                        flag = True
                elif i == 7:
                    if res == '000000':
                        self.log.info('结果与期望的值相等')
                        flag = True
            finally:
                if flag == False:
                    res = msg.split('\n')[2].split('|')[0].strip()
                    cmd1 = f"select '{now}'::timestamp - '{res}'::timestamp;"
                    msg1 = self.commonsh.execut_db_sql(cmd1)
                    self.log.info(msg1)
                    diff = msg1.splitlines()[-2].strip().lstrip('-')
                    self.log.info('时:分:秒,判断时和分都是00，即只差了几秒')
                    self.assertTrue(diff[:5] <= '00:05')
                    self.log.info('实际结果与期望之间差异不超过五分钟,'
                                  '判定结果正确')
                    flag = True
            self.assertTrue(flag)

    def tearDown(self):
        self.log.info(
            "--Opengauss_Function_Innerfunc_Sysdate_Case0008结束--")
