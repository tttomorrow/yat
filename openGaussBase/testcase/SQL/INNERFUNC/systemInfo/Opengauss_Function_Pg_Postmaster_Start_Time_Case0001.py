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
Case Name   : pg_postmaster_start_time函数返回服务器启动时间
Description :
    步骤 1.重启数据库
    步骤 2. 执行函数pg_postmaster_start_time获取重启数据库时的时间戳
    步骤 3.函数返回值为字符串类型，转化为python时间戳
    步骤 4.获取当前时间的时间戳，求pg_postmaster_start_time函数返回值时间戳
          与当前时间戳的差值,预期差值小于5min
Expect      :
    步骤 1.重启成功
    步骤 2.函数执行成功，获取重启数据库时的时间戳成功
    步骤 3.字符串类型，转化为python时间戳成功
    步骤 4.成功
"""
import os
import unittest
from datetime import datetime

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Innerfunc01(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info(f'-----{os.path.basename(__file__)} start-----')

    def test_pg_postmaster_start_time(self):
        text1 = '--step1: 重启数据库;expect: 重启数据库成功--'
        self.log.info(text1)
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status('detail')
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text1)

        text2 = '---step2: 执行函数pg_postmaster_start_time获取重启数据库时' \
                '的时间戳;expect: 函数执行成功，获取重启数据库时的时间戳成功--'
        self.log.info(text2)
        sql_res = self.commonsh.execut_db_sql(
            ' select substring (pg_postmaster_start_time(),0,20);')
        self.log.info(sql_res)
        self.assertIn('substring', sql_res, '执行失败:' + text2)
        self.log.info('获取重启数据库的时间戳')
        date_res1 = sql_res.splitlines()[-2].strip()
        self.log.info(date_res1)

        text3 = f'--step3:函数返回值为字符串类型，转化为python时间戳; ' \
                f'expect: 字符串类型，转化为python时间戳成功-----'
        self.log.info(text3)
        date_before = datetime.strptime(date_res1, "%Y-%m-%d %H:%M:%S")

        text4 = f'---step4: 获取当前时间的时间戳，求pg_postmaster_start_time' \
                f'函数返回值时间戳与当前时间戳的差值,预期差值小于5min' \
                f'（因可能存在整点整年的跳转，故采取时间差断言）; ' \
                f'expect: 成功-----'
        self.log.info(text4)
        sql_res = self.commonsh.execut_db_sql('select sysdate;')
        self.log.info(sql_res)
        self.assertIn('sysdate', sql_res, '执行失败:' + text4)
        self.log.info('获取当前时间戳')
        date_res2 = sql_res.splitlines()[-2].strip()
        self.log.info(date_res2)
        self.log.info('sysdate()函数返回值为字符串类型，转化为python时间戳;')
        date_now = datetime.strptime(date_res2, "%Y-%m-%d %H:%M:%S")
        timing_vari = date_now - date_before
        self.log.info(timing_vari)
        self.log.info('将时间差转换为秒')
        sec_time = timing_vari.seconds
        self.log.info(sec_time)
        self.assertLessEqual(sec_time, 300, '执行失败:' + text4)

    def tearDown(self):
        self.log.info('-----无需清理环境-----')
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
