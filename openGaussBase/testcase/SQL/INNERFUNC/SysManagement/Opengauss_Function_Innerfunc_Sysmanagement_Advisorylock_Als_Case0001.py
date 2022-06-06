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
Case Name   : pg_advisory_lock_shared(key bigint)获取会话级别的共享咨询锁
Description :
    1.创建表,使用一个唯一ID(用于advisory lock)插入数据
    2.会话1，使用advisory lock锁住这个ID,并更新数据;查询数据
    3.会话2，读取上面的记录
    4.会话1提交事务
    5.会话2再次查询
    6.会话1，开启事务，更新这条记录的同时使用advisory lock锁住这个ID，查询数据
    7.会话3对该id也进行加锁、修改
    8.会话1中提交事务
    9.会话3中查询
    10.清理环境
Expect      :
    1.创建成功;数据插入成功
    2.加锁成功，数据更新成功
    3.查询到的是未更新过的数据
    4.提交成功
    5.会话2查询到了更新后的数据
    6.加锁成功，查询到数据更新成功
    7.在会话1关闭事务前，会话2的update语句处于等待状态
    8.提交成功
    9.update成功;查询到的是修改后的数据
    10.清理环境完成
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
            '-Opengauss_Function_Innerfunc_Sysmanagement_Advisorylock_Als_'
            'Case0001 start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = 'tb_advisorylock_al_case0003'

    def test_advisorylock(self):
        step1_txt = '---step1:创建表,使用一个唯一ID(用于advisory lock),' \
                    '插入数据;expect:创建成功;数据插入成功---'
        self.log.info(step1_txt)
        sql_cmd1 = f"drop table if exists {self.tb_name};" \
                   f"create table {self.tb_name}(id int8 primary key, " \
                   f"info text);" \
                   f"insert into {self.tb_name} values(2, 'test');"

        step2_txt = '---step2:会话1，开启事务，使用advisory lock锁住这个ID，' \
                    '并更新数据;查询数据;' \
                    'expect:加锁成功，数据更新成功---'
        self.log.info(step2_txt)
        sql_cmd2 = f"start transaction;" \
                   f"select pg_advisory_lock_shared(id) from " \
                   f"tb_advisorylock_al_case0003;" \
                   f"update {self.tb_name} set info='abc' where id=2;" \
                   f"select * from {self.tb_name} where id=2;"

        step3_txt = '---step3:会话2，读取上面的记录;' \
                    'expect:查询到的是未更新过的数据---'
        self.log.info(step3_txt)
        sql_cmd3 = f"select * from {self.tb_name} where id=2;"

        step4_txt = '--step4:会话1提交事务;expect:提交成功--'
        self.log.info(step4_txt)
        sql_cmd4 = "commit;"

        step5_txt = '--step5:会话2再次查询;expect:会话2查询到了更新后的数据--'
        self.log.info(step5_txt)
        sql_cmd5 = f"select * from {self.tb_name} where id=2;"

        step6_txt = '---step6:会话1，开启事务，更新这条记录的同时，' \
                    '使用advisory lock锁住这个ID，查询数据;' \
                    'expect:加锁成功，查询到数据更新成功---'
        self.log.info(step6_txt)
        sql_cmd6 = f"start transaction;" \
                   f"select pg_advisory_lock_shared(id) from {self.tb_name};" \
                   f"update {self.tb_name} set info='bbb' where id=2;" \
                   f"select * from {self.tb_name} where id=2;"

        step7_txt = '--step7:会话3对该id也进行加锁、修改;' \
                    'expect:在会话1关闭事务前，会话2的update语句处于等待状态--'
        self.log.info(step7_txt)
        sql_cmd7 = f"start transaction;" \
                   f"select pg_advisory_lock_shared(id) from {self.tb_name};" \
                   f"select timenow();" \
                   f"update {self.tb_name} set info='ABC' where id=2;" \
                   f"select timenow();"

        step8_txt = '---step8:会话1中提交事务;expect:提交成功---'
        self.log.info(step8_txt)
        sql_cmd8 = "commit;"

        step9_txt = '---step9:会话3中查询;expect:update成功;' \
                    '查询到的是修改后的数据---'
        self.log.info(step9_txt)
        sql_cmd9 = f"select * from {self.tb_name} where id=2;"

        threads = []
        self.log.info('----线程1操作事务1:step1->step2->step4->step6->step8--')
        tras_sql1 = f'select timenow();' \
                    f'{sql_cmd1}' \
                    f'{sql_cmd2}' \
                    f'select pg_sleep(15);' \
                    f'{sql_cmd4}' \
                    f'select pg_sleep(20);' \
                    f'{sql_cmd6};' \
                    f'select pg_sleep(100);' \
                    f'{sql_cmd8}'
        session1 = ComThread(self.pri_sh.execut_db_sql, args=(tras_sql1,))
        threads.append(session1)

        self.log.info('----线程2操作事务2:step3->step5----')
        tras_sql2 = f'select timenow();' \
                    f'select pg_sleep(11);' \
                    f'{sql_cmd3}' \
                    f'select pg_sleep(15);' \
                    f'{sql_cmd5}'
        session2 = ComThread(self.pri_sh.execut_db_sql, args=(tras_sql2,))
        threads.append(session2)

        self.log.info('----线程3操作事务3:step7->step9----')
        tras_sql3 = f'select timenow();' \
                    f'select pg_sleep(60);' \
                    f'{sql_cmd7}' \
                    f'select pg_sleep(80);' \
                    f'{sql_cmd9}'
        session3 = ComThread(self.pri_sh.execut_db_sql, args=(tras_sql3,))
        threads.append(session3)

        self.log.info('----启动线程----')
        thread_results = []
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join(300)
            thread_results.append(t.get_result())
            self.log.info(t.get_result())
        self.log.info('获取线程结果')
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG,
                      thread_results[0], '执行失败:' + step2_txt)
        self.assertIn('2 | abc', thread_results[0].splitlines()[19].strip(),
                      '执行失败:' + step2_txt)
        self.assertIn('2 | test', thread_results[1].splitlines()[12].strip(),
                      '执行失败:' + step3_txt)
        self.assertEqual(self.constant.COMMIT_SUCCESS_MSG,
                         thread_results[0].splitlines()[27].strip(),
                         '执行失败:' + step4_txt)
        self.assertEqual('2 | abc', thread_results[1].splitlines()[-2].strip(),
                         '执行失败:' + step5_txt)
        self.assertEqual('2 | bbb', thread_results[0].splitlines()[-9].strip(),
                         '执行失败:' + step6_txt)
        self.assertEqual('2 | ABC', thread_results[2].splitlines()[-2].strip(),
                         '执行失败:' + step6_txt)

        self.log.info('分别获取step7中update阻塞前及update成功后的时间')
        start_time = thread_results[2].splitlines()[-18].strip()[:-3]
        self.log.info(start_time)
        trans_to_dtime1 = datetime.datetime.strptime(start_time,
                                                     '%Y-%m-%d %H:%M:%S')
        self.log.info(f'step7会话3执行update阻塞前的时间为:{trans_to_dtime1}')
        end_time = thread_results[2].splitlines()[-12].strip()[:-3]
        self.log.info(end_time)
        trans_to_dtime2 = datetime.datetime.strptime(end_time,
                                                     '%Y-%m-%d %H:%M:%S')
        self.log.info(f'step8中会话1提交，会话3update成功，'
                      f'时间为:{trans_to_dtime2}')
        self.log.info('计算会话3中update执行成功的前后阻塞时间')
        time_diff = trans_to_dtime2 - trans_to_dtime1
        self.log.info(time_diff)
        num = str(time_diff).split(':')[-1]
        self.log.info(f'阻塞时间为{num}')
        self.assertGreaterEqual(f'{num}', '02', '执行失败:' + step7_txt)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG,
                      thread_results[0].splitlines()[-1].strip(),
                      '执行失败:' + step8_txt)
        self.assertEqual('2 | ABC', thread_results[2].splitlines()[-2].strip(),
                         '执行失败:' + step9_txt)

    def tearDown(self):
        text = '---step10:清理环境;expect:清理环境完成---'
        self.log.info(text)
        self.log.info('删除表')
        drop_msg = self.pri_sh.execut_db_sql(f"drop table if exists "
                                             f"{self.tb_name};")
        self.log.info(drop_msg)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Innerfunc_Sysmanagement_Advisorylock_'
            'Als_Case0001 finish-')
