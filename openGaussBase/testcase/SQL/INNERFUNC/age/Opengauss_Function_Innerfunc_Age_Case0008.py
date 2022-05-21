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
Case Name   : 使用age(timestamp)函数返回当前时间与参数相减的结果
Description : age(timestamp)描述：当前时间和参数相减。返回值类型：interval
    1.入参给timestamp without time zone、timestamp with time zone
    2.异常校验
Expect      :
    1.函数返回结果正确
    2.异常报错
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Function(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("---Opengauss_Function_Innerfunc_Age_Case0008开始执行---")
        self.commonsh = CommonSH('dbuser')

    def test_age(self):
        text = 'step1:获取前一天时间;expect:获取成功'
        self.log.info(text)
        get_time = self.commonsh.execut_db_sql("select current_date - "
                                               "interval '1 day' as result;")
        self.log.info(get_time)
        last_day = get_time.splitlines()[2].strip().split()[0]
        self.log.info('last_day' + last_day)

        text = 'step2:使用age函数计算当前时间与前一天时间相减;expect:计算正确'
        self.log.info(text)
        sql_cmd = f"select age(timestamp '{last_day}');" \
                  f"select age(timestamp '{last_day + ' 00:00:00'}');" \
                  f"select age(timestamp '{last_day + ' 00:00:00.00+01'}');"
        msg = self.commonsh.execut_db_sql(sql_cmd)
        self.log.info(msg)
        self.assertTrue(msg.count('1 day') == 3, '执行失败:' + text)

        text = 'step3:函数错误调用;expect:合理报错'
        self.log.info(text)
        cmd = "select age();  select age(interval '5 seconds');"
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        self.assertTrue(msg.count('ERROR') == 2, '执行失败:' + text)

    def tearDown(self):
        self.log.info('---Opengauss_Function_Innerfunc_Age_Case0008执行结束---')
