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
Case Name   : 使用to_char函数对当前时间戳进行指定格式的输出
Description :
    1.to_char函数将timestamp with time zone转换为指定的格式输出
Expect      :
    1.函数返回结果正确
"""

import unittest

from yat.test import Node

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("Opengauss_Function_Innerfunc_To_Char_Case0001开始")
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_age(self):
        LOG.info('入参指定输出格式')
        text = ['HH12:MI', 'mm-dd-yyyy HH24:MI', 'Dy Mon DD HH24:MI:SS yyyy']
        for i in range(3):
            cmd = f"""select to_char(current_timestamp, '{text[i]}');"""
            LOG.info(cmd)
            msg = self.commonsh.execut_db_sql(cmd)
            LOG.info(msg)
            res = msg.splitlines()[2].strip()
            LOG.info('--输出当前时间：' + res)
            if i == 0:
                hour, mins = res.split(':')[0], res.split(':')[1]
                self.assertTrue(len(res) <= 5 and
                                1 <= int(hour) <= 12 and 0 <= int(mins) <= 59)
            elif i == 1:
                LOG.info('--使用date获取当前时间为月日年 时分格式--')
                get_date = self.user.sh('date +"%m-%d-%Y %H:%M"').result()
                LOG.info(get_date)
                now_1 = res.split()[0].strip()
                LOG.info(now_1)
                month, day, year = list(map(int, now_1.split('-')))
                self.assertTrue(now_1 == res or (
                        0 < year and
                        1 <= int(month) <= 12 and
                        1 <= int(day) <= 31))
                time1 = res.split()[1].strip()
                hour, mins = time1.split(':')
                self.assertTrue(0 <= int(hour) <= 23 and 0 <= int(mins) <= 59)
            elif i == 2:
                LOG.info('--获取当前时间格式为Dy Mon DD HH24:MI:SS yyyy--')
                get_date = self.user.sh('date').result()
                LOG.info(get_date)
                now_2 = get_date.strip().split()
                LOG.info(now_2)
                del now_2[-2]
                if now_2[-5:] == res[-5:] and (
                        now_2 == res or
                        now_2[:17].replace(' ', '0') == res[:17].replace(' ',
                                                                         '0')):
                    LOG.info('年相等并且前面的时间(不带秒)相等')
                else:
                    db_time = res.split()[3]
                    LOG.info(db_time)
                    get_date = self.user.sh('date').result()
                    LOG.info(get_date)
                    sys_time = get_date.strip().split()[3]
                    LOG.info(sys_time)
                    cmd2 = f"select '{db_time}'::interval - " \
                           f"'{sys_time}'::interval;"
                    LOG.info(cmd2)
                    msg2 = self.commonsh.execut_db_sql(cmd2)
                    LOG.info(msg2)
                    diff = msg2.split('\n')[-2].split()[-1].strip().strip('-')
                    self.assertTrue(diff[:5] <= '00:05')

    def tearDown(self):
        LOG.info("Opengauss_Function_Innerfunc_To_Char_Case0001结束")
