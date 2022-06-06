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
Case Name   : pg_try_advisory_xact_lock_shared(key bigint)尝试获取事务级别的共
             享咨询锁
Description :
    1.创建表,插入数据
    2.会话1，更新这条记录的同时，使用advisory lock锁住这个ID并查询;
    3.会话2，读这条记录
    4.会话2先对该id也进行加锁
    5.会话1提交事务
    6.会话2提交事务
    7.清理环境
Expect      :
    1.创建成功;数据插入成功
    2.加锁成功，表数据更新成功
    3.读写不冲突，查询成功，数据未更新
    4.在会话1未提交事务之前，会话2加锁成功,更新语句处于等待的状态
    5.提交成功;会话2更新数据成功
    6.提交成功
    7.清理环境完成
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
            '-Opengauss_Function_Innerfunc_Sysmanagement_Advisorylock_Taxls_'
            'Case0001 start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = 'tb_advisorylock_taxls_case0001'

    def test_advisorylock(self):
        step1_txt = '---step1:创建表,插入数据;expect:创建成功;数据插入成功---'
        self.log.info(step1_txt)
        sql_cmd = f"drop table if exists {self.tb_name};" \
                  f"create table {self.tb_name}(id int primary key, " \
                  f"info text);" \
                  f"insert into {self.tb_name} values(2, 'test');"
        execute_cmd = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(execute_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, execute_cmd,
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, execute_cmd,
                      '执行失败:' + step1_txt)

        step2_txt = '会话1执行以下操作'
        self.log.info(step2_txt)
        self.log.info('-step2.1:会话1，更新这条记录的同时，使用advisory lock'
                      '锁住这个ID并查询;expect:加锁成功，表1数据更新成功-')
        self.log.info('--step2.2:查询')
        self.log.info('--step2.3:会话1提交事务;expect:提交成功;'
                      '会话2更新数据成功-')
        sql_cmd = f"start transaction;" \
                  f"update {self.tb_name} set info='mmm' where id=2  " \
                  f"returning pg_try_advisory_xact_lock_shared(id);" \
                  f"select * from {self.tb_name} where id=2;" \
                  f"select pg_sleep(10);" \
                  f"commit;"
        thread_1 = ComThread(self.pri_sh.execut_db_sql, args=(sql_cmd, ''))
        thread_1.setDaemon(True)
        thread_1.start()

        step3_txt = '会话2执行以下操作'
        self.log.info(step3_txt)
        self.log.info('---step3.1:会话2，读这条记录;expect:读写不冲突，'
                      '查询成功，数据未更新--;')
        self.log.info('--step3.2:会话2先对该id也进行加锁;'
                      'expect:在会话1未提交事务之前，会话2加锁成功,'
                      '更新语句处于等待的状态--')
        self.log.info(step3_txt)
        sql_cmd = f"select pg_sleep(3);" \
                  f"select * from {self.tb_name} where id=2;" \
                  f"start transaction;" \
                  f"select timenow();" \
                  f"update {self.tb_name} set info='ABC' where id=2 " \
                  f"returning pg_try_advisory_xact_lock_shared(id);" \
                  f"select timenow();" \
                  f"select pg_sleep(20);" \
                  f"commit;"
        thread_2 = ComThread(self.pri_sh.execut_db_sql, args=(sql_cmd, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        thread_1.join(10 * 60)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)
        msg1 = msg_result_1.splitlines()
        self.log.info(msg1)

        thread_2.join(10 * 60)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)
        msg2 = msg_result_2.splitlines()
        self.log.info(msg2)

        self.log.info('获取线程结果')
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG,
                      msg_result_1, '执行失败:' + step2_txt)
        self.assertIn('t', msg_result_1, '执行失败:' + step2_txt)
        self.assertIn('UPDATE 1', msg_result_1, '执行失败:' + step2_txt)
        self.assertIn('2 | mmm', msg_result_1.splitlines()[-9].strip(),
                      '执行失败:' + step2_txt)
        self.assertIn('2 | test', msg_result_2.splitlines()[7].strip(),
                      '执行失败:' + step3_txt)
        self.log.info('分别获取step3中更新前及更新成功后的时间')
        start_time = msg_result_2.splitlines()[13].strip()[:-3:]
        self.log.info(start_time)
        trans_to_dtime1 = datetime.datetime.strptime(start_time,
                                                     '%Y-%m-%d %H:%M:%S')
        end_time = msg_result_2.splitlines()[-9].strip()[:-3:]
        self.log.info(end_time)
        trans_to_dtime2 = datetime.datetime.strptime(end_time,
                                                     '%Y-%m-%d %H:%M:%S')
        self.log.info('计算会话2中加锁执行成功的阻塞时间')
        time_diff = trans_to_dtime2 - trans_to_dtime1
        self.log.info(time_diff)
        num = str(time_diff).split(':')[-1]
        self.log.info(f'阻塞时间为{num}')
        self.assertTrue(f'{num} > = 05', '执行失败:' + step3_txt)

    def tearDown(self):
        text = '---step4:清理环境;expect:清理环境完成---'
        self.log.info(text)
        self.log.info('删除表')
        drop_msg = self.pri_sh.execut_db_sql(f"drop table if exists "
                                             f"{self.tb_name};")
        self.log.info(drop_msg)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Innerfunc_Sysmanagement_Advisorylock_'
            'Taxls_Case0001 finish-')
