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
Case Type   : 内建函数
Case Name   : pg_advisory_lock(key bigint)获取会话级别的排它咨询锁
Description :
    1.创建表,使用一个唯一ID(用于advisory lock);插入数据
    2.会话1，更新这条记录的同时，使用advisory lock锁住这个ID
    3.会话2，再次执行加锁
    4.获取step2和step3结果
    5.清理环境
Expect      :
    1.创建成功;数据插入成功
    2.数据更新成功，加锁成功
    3.在会话1未关闭时，会话2加锁处于阻塞状态，
    会话1关闭，会话2由阻塞状态变为加锁成功
    4.获取成功
    5.清理环境成功
History     :
"""

import datetime
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Innerfunc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Innerfunc_Sysmanagement_Advisorylock_Al_'
            'Case0001 start-')
        self.constant = Constant()
        self.pri_sh1 = CommonSH('PrimaryDbUser')
        self.pri_sh2 = CommonSH('PrimaryDbUser')
        self.tb_name = 'tb_advisorylock_al_case0001'

    def test_advisorylock(self):
        step1_txt = '---step1:创建表,使用一个唯一ID(用于advisory lock),' \
                    '插入数据;expect:创建成功;数据插入成功---'
        self.log.info(step1_txt)
        sql_cmd = self.pri_sh1.execut_db_sql(f"drop table if exists "
                                             f"{self.tb_name};"
                                             f"create table {self.tb_name}"
                                             f"(id int8 primary key, "
                                             f"info text);"
                                             f"insert into {self.tb_name} "
                                             f"values(1, 'test');")
        self.log.info(sql_cmd)
        self.assertTrue(self.constant.TABLE_CREATE_SUCCESS in sql_cmd and
                        self.constant.INSERT_SUCCESS_MSG in sql_cmd,
                        '执行失败:' + step1_txt)

        step2_txt = '---step2:会话1，更新这条记录的同时，使用advisory lock' \
                    '锁住这个id;expect:数据更新成功，加锁成功---'
        self.log.info(step2_txt)
        sql_cmd = f"start transaction;" \
                  f"update {self.tb_name} set info='abc' where id=1 " \
                  f"returning pg_advisory_lock(id);" \
                  f"select pg_sleep(15);"
        self.log.info(sql_cmd)
        thread_1 = ComThread(self.pri_sh1.execut_db_sql, args=(sql_cmd, ''))
        thread_1.setDaemon(True)
        thread_1.start()

        step3_txt = '---step3:会话2，再次执行加锁;' \
                    'expect:在会话1未关闭时，会话2加锁处于阻塞状态;' \
                    '会话1关闭，会话2由阻塞状态变为加锁成功---'
        self.log.info(step3_txt)
        sql_cmd = "select pg_sleep(3);" \
                  "select timenow();" \
                  "select pg_advisory_lock(1);" \
                  "select timenow();"
        self.log.info(sql_cmd)
        thread_2 = ComThread(self.pri_sh2.execut_db_sql, args=(sql_cmd, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        step4_txt = '--step4:获取step2和step3结果;expect:获取成功;' \
                    '阻塞时间见断言--'
        self.log.info(step4_txt)
        thread_1.join(30)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)
        self.assertIn('START TRANSACTION', msg_result_1,
                      '执行失败:' + step2_txt)
        self.assertIn('UPDATE 1', msg_result_1, '执行失败:' + step2_txt)

        thread_2.join(30)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)
        msg = msg_result_2.splitlines()
        self.log.info(msg)
        self.log.info('分别获取step3中加锁阻塞前及加锁执行成功后的时间')
        start_time = msg_result_2.splitlines()[7].strip()[:-3]
        self.log.info(start_time)
        trans_to_dtime1 = datetime.datetime.strptime(start_time,
                                                     '%Y-%m-%d %H:%M:%S')
        end_time = msg_result_2.splitlines()[-2].strip()[:-3]
        self.log.info(end_time)
        trans_to_dtime2 = datetime.datetime.strptime(end_time,
                                                     '%Y-%m-%d %H:%M:%S')
        self.log.info('计算会话2中加锁执行成功的前后阻塞时间')
        time_diff = trans_to_dtime2 - trans_to_dtime1
        self.log.info(time_diff)
        num = str(time_diff).split(':')[-1]
        self.log.info(f'阻塞时间为{num}')
        self.assertGreaterEqual(f'{num}', '11', '执行失败:' + step3_txt)
        self.assertEqual('(1 row)', msg_result_2.splitlines()[-1].strip(),
                         '执行失败:' + step3_txt)

    def tearDown(self):
        text = '---step5:清理环境;expect:清理环境完成---'
        self.log.info(text)
        self.log.info('删除表')
        drop_msg = self.pri_sh1.execut_db_sql(f"drop table if exists "
                                              f"{self.tb_name};")
        self.log.info(drop_msg)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Innerfunc_Sysmanagement_Advisorylock_'
            'Axl_Case0001 finish-')
