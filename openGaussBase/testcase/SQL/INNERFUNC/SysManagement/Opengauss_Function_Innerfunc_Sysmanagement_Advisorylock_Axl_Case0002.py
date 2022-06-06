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
Case Name   : pg_advisory_xact_lock(key1 int, key2 int)获取事务级别的排它咨询锁
Description :
    1.创建表,插入数据
    2.会话1，更新这条记录的同时，使用advisory lock锁住这个ID
    3.会话2，再次执行加锁
    4.会话1，commit事务
    5.清理环境
Expect      :
    1. 表创建成功 数据插入成功
    2. 数据更新成功，加锁成功
    3. 在会话1未提交事务时，会话2加锁处于等待状态
    4. 会话1提交事务后，会话2中加锁成功
    5. 清理环境完成
              避免执行sql语句时间执行顺序变化，导致断言失败
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
            '-Opengauss_Function_Innerfunc_Sysmanagement_Advisorylock_Axl_'
            'Case0002 start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = 'tb_advisorylock_axl_case0002'
        self.tb_name_01 = 'tb_advisorylock_axl_case0002_01'

    def test_advisorylock(self):
        step1_txt = '---step1:创建表,插入数据;expect:创建成功;数据插入成功---'
        self.log.info(step1_txt)
        sql_cmd1 = f"drop table if exists {self.tb_name};" \
                   f"drop table if exists {self.tb_name_01};" \
                   f"create table {self.tb_name}" \
                   f"(id int4 primary key, info text);" \
                   f"insert into {self.tb_name} values (1,'test');" \
                   f"create table {self.tb_name_01}" \
                   f"(id int4 primary key, info text);" \
                   f"insert into {self.tb_name_01} values (1,'test');"

        step2_txt = '---step2:会话1,更新这条记录的同时，使用advisory lock' \
                    '锁住这个ID;expect:数据更新成功，加锁成功---'
        self.log.info(step2_txt)
        sql_cmd2 = f"start transaction;" \
                   f" update {self.tb_name} set info='abc' where id=1 " \
                   f"returning pg_advisory_xact_lock(id,id);"

        step3_txt = '---step3:会话2，再次执行加锁;' \
                    'expect:在会话1未提交事务时，会话2加锁处于等待状态--'
        self.log.info(step3_txt)
        sql_cmd3 = f"select pg_advisory_xact_lock(1,1);"

        step4_txt = '--step4:会话1，commit上个事务;expect:提交成功;' \
                    '会话2由等待状态变为加锁成功--'
        self.log.info(step4_txt)
        sql_cmd4 = "commit;"

        threads = []
        self.log.info('----线程1操作事务1:step1->step2->step4--')
        tras_sql1 = f'{sql_cmd1}' \
                    f'{sql_cmd2}' \
                    f'select pg_sleep(30);' \
                    f'select timenow();' \
                    f'{sql_cmd4}' \
                    f'select timenow();'
        session1 = ComThread(self.pri_sh.execut_db_sql, args=(tras_sql1,))
        threads.append(session1)

        self.log.info('----线程2操作事务2:step3-')
        tras_sql2 = f'select pg_sleep(20);' \
                    f'select timenow();' \
                    f'{sql_cmd3}' \
                    f'select timenow();'
        session2 = ComThread(self.pri_sh.execut_db_sql, args=(tras_sql2,))
        threads.append(session2)

        self.log.info('----启动线程----')
        thread_results = []
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join(120)
            thread_results.append(t.get_result())
            self.log.info(t.get_result())
        self.log.info('获取线程结果')
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG,
                      thread_results[0], '执行失败:' + step2_txt)
        self.assertIn(self.constant.UPDATE_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step2_txt)

        self.log.info('分别获取step3中加锁阻塞前及加锁成功后的时间')
        start_time = thread_results[1].splitlines()[-12].strip()[:-3:]
        self.log.info(start_time)
        trans_to_dtime1 = datetime.datetime.strptime(start_time,
                                                     '%Y-%m-%d %H:%M:%S')
        end_time = thread_results[1].splitlines()[-2].strip()[:-3:]
        self.log.info(end_time)
        trans_to_dtime2 = datetime.datetime.strptime(end_time,
                                                     '%Y-%m-%d %H:%M:%S')
        self.log.info('计算会话2中加锁执行成功的阻塞时间')
        time_diff = trans_to_dtime2 - trans_to_dtime1
        self.log.info(time_diff)
        num = str(time_diff).split(':')[-1]
        self.log.info(f'阻塞时间为{num}')
        self.assertGreater(f'{num}', '00', '执行失败:' + step3_txt)

    def tearDown(self):
        text = '---step5:清理环境;expect:清理环境完成---'
        self.log.info(text)
        self.log.info('删除表')
        drop_msg = self.pri_sh.execut_db_sql(f"drop table if exists "
                                             f"{self.tb_name};"
                                             f"drop table if exists "
                                             f"{self.tb_name_01};")
        self.log.info(drop_msg)
        self.assertTrue(drop_msg.count(self.constant.DROP_TABLE_SUCCESS) == 2,
                        '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Innerfunc_Sysmanagement_Advisorylock_'
            'Axl_Case0002 finish-')
