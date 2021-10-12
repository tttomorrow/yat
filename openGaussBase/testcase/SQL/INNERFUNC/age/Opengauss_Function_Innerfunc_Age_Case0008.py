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
Case Name   : 使用age(timestamp)函数返回当前时间与参数相减的结果
Description : age(timestamp)描述：当前时间和参数相减。返回值类型：interval
    1.入参给timestamp without time zone、timestamp with time zone
    2.异常校验
Expect      :
    1.函数返回结果正确
    2.异常报错
History     :
"""

import unittest
import time
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        logger.info("---Opengauss_Function_Innerfunc_Age_Case0008开始执行---")
        self.commonsh = CommonSH('dbuser')

    def test_age(self):
        # 测试点1：入参区分带时区、带时间
        timestamp = ['1957-06-13', '2001-02-16 20:38:40',
                     '2017-09-01 16:57:36.636205+08']
        for i in range(3):
            cmd = f"""select age(timestamp '{timestamp[i]}');"""
            msg = self.commonsh.execut_db_sql(cmd)
            logger.info(msg)
            res = msg.splitlines()[2].strip()
            # 63 years 7 mons
            # 3 years 4 mons 6 days 07:02:23.363795
            res_list = res.split()
            # timestamp后面两个带时间
            self.assertTrue(len(res_list) >= 4)
            # 判断返回格式里的关键字
            self.assertTrue('years' in msg or 'mons' in msg or 'days' in msg)
            # 判断对应年月日值是否是数字
            pre = len(res_list) - 1
            s = [res_list[i].isdigit() for i in range(pre) if i % 2 == 0]
            self.assertTrue(s.count(True) >= 2 and s.count(True) == len(s))

        # 测试点2：错误调用
        cmd1 = '''select age();  select age(interval '5 seconds');'''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        logger.info(msg1)
        self.assertTrue(msg1.count('ERROR') == 2)

    def tearDown(self):
        logger.info('---Opengauss_Function_Innerfunc_Age_Case0008执行结束---')