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
Case Name   : 使用timeofday()函数获取当前日期及时间
Description : timeofday()描述：当前日期及时间。返回值类型：text
    1.正常获取
    2.错误调用
Expect      :
    1.获取正确
    2.异常报错
              time.ctime获取当前时间改为date;
"""
import unittest

from yat.test import Node

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("Opengauss_Function_Innerfunc_Timeofday_Case0001开始")
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_time(self):
        LOG.info('----正常使用函数timeofday获取当前日期及时间----')
        cmd = '''select timeofday();'''
        LOG.info(cmd)
        msg = self.commonsh.execut_db_sql(cmd)
        LOG.info(msg)
        db_time = msg.splitlines()[2].strip().split()
        LOG.info("['Wed', 'Jul', '28', '11:53:33.654416', '2021', 'CST']")
        LOG.info(db_time)
        LOG.info('----使用date获取当前时间---')
        get_date = self.user.sh('date').result()
        LOG.info(get_date)
        now = get_date.strip().split()
        LOG.info("显示格式 ['Wed', 'Jul', '28', '11:53:33', 'CST', '2021']")
        LOG.info(now)
        if int(now[2]) < 10:
            now[2] = '0' + now[2]
        LOG.info(' 判断长度、含年月日星期时间及时区')
        self.assertTrue(len(db_time) == 6)
        LOG.info('时区')
        self.assertTrue(db_time[-1] == 'CST')
        LOG.info('年')
        self.assertTrue(db_time[-2] == now[-1])
        LOG.info('日 月 星期')
        self.assertTrue(db_time[:3] == now[:3])
        cmd2 = f"select '{db_time[3]}'::interval - '{now[3]}'::interval;"
        LOG.info(cmd2)
        msg2 = self.commonsh.execut_db_sql(cmd2)
        LOG.info(msg2)
        diff = msg2.splitlines()[-2].split()[-1].strip().strip('-')
        self.assertTrue(diff[:5] <= '00:05')
        LOG.info('---测试点2：错误调用---')
        cmd1 = 'select timeofday; select timeofday(8);'
        msg1 = self.commonsh.execut_db_sql(cmd1)
        LOG.info(msg1)
        self.assertTrue(msg1.count('ERROR') == 2)

    def tearDown(self):
        LOG.info("Opengauss_Function_Innerfunc_Timeofday_Case0001结束")
