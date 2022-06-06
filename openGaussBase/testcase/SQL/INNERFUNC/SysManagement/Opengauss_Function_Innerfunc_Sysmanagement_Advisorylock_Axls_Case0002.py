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
Case Name   : pg_advisory_xact_lock_shared(key1 int, key2 int)获取事务级别的
             共享咨询锁
Description :
    1.创建表,插入数据
    2.会话1，使用advisory lock锁住这个ID并更新数据
    3.会话1更新数据并查询
    4.会话2查询
    5.会话2对该id也进行加锁
    6.会话2修改表数据
    7.会话1提交事务
    8.会话2对表2进行更新和查询
    9.会话2提交事务
    10.清理环境
Expect      :
    1.创建成功;数据插入成功
    2.加锁成功
    3.更新成功
    4.数据未更新
    5.会话2加锁成功
    6.会话1未提交事务，修改处于等待状态
    7.提交成功;step6表更新成功
    8.表2的数据更新不受限制
    9.提交成功
    10.清理环境完成
              避免执行sql语句时间执行顺序变化，导致断言失败；
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
            '-Opengauss_Function_Innerfunc_Sysmanagement_Advisorylock_Axls_'
            'Case0002 start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = 'tb_advisorylock_axls_case0002'
        self.tb_name_01 = 'tb_advisorylock_axls_case0002_01'

    def test_advisorylock(self):
        step1_txt = '---step1:创建表,插入数据;expect:创建成功;数据插入成功---'
        self.log.info(step1_txt)
        sql_cmd1 = f"drop table if exists {self.tb_name};" \
                   f"create table {self.tb_name}" \
                   f"(qq int primary key, class text);" \
                   f"insert into {self.tb_name} values (2,'test');" \
                   f"create table {self.tb_name_01}" \
                   f"(qq int primary key, class text);" \
                   f"insert into {self.tb_name_01} values (2,'test');"

        step2_txt = '---step2:会话1，使用advisory lock锁住这个qq' \
                    ';expect:加锁成功---'
        self.log.info(step2_txt)
        sql_cmd2 = f"start transaction;" \
                   f"select pg_advisory_xact_lock_shared(qq,qq) from " \
                   f"{self.tb_name};"

        step3_txt = '---step3:会话1更新数据并查询;expect:更新成功---'
        self.log.info(step3_txt)
        sql_cmd3 = f"update {self.tb_name} set class='mmm' where qq=2;" \
                   f"select * from {self.tb_name};"

        step4_txt = '---step4:会话2查询;expect:数据未更新---'
        self.log.info(step4_txt)
        sql_cmd4 = f"select * from {self.tb_name};"

        step5_txt = '--step5:会话2对先对该qq也进行加锁;' \
                    'expect:在会话1未提交事务之前，会话2加锁成功--'
        self.log.info(step5_txt)
        sql_cmd5 = f"start transaction;" \
                   f"select pg_advisory_xact_lock_shared(qq,qq) from " \
                   f"{self.tb_name};"

        step6_txt = '--step6:会话2修改数据;expect:会话1未提交事务，' \
                    '修改处于等待状态'
        self.log.info(step6_txt)
        sql_cmd6 = f"update {self.tb_name} set class='ABC' where qq=2;"

        step7_txt = '---step7:会话1提交事务;expect:提交成功;step6表更新成功-'
        self.log.info(step7_txt)
        sql_cmd7 = "commit;"

        step8_txt = '--step8:会话2对表2进行更新和查询;' \
                    'expect:表2的数据更新不受限制'
        self.log.info(step8_txt)
        sql_cmd8 = f"update {self.tb_name_01} set class='mmm' where qq=2;"

        step9_txt = '---step9:会话2提交事务;expect:提交成功---'
        self.log.info(step9_txt)
        sql_cmd9 = "commit;"

        threads = []
        self.log.info('----线程1操作事务1:step1->step2->step3->step7-')
        tras_sql1 = f'{sql_cmd1}' \
                    f'{sql_cmd2}' \
                    f'{sql_cmd3}' \
                    f'select pg_sleep(25);' \
                    f'{sql_cmd7}'
        session1 = ComThread(self.pri_sh.execut_db_sql, args=(tras_sql1,))
        threads.append(session1)

        self.log.info('----线程2操作事务2:step4->step5->step6->step8->step9--')
        tras_sql2 = f'select pg_sleep(20);' \
                    f'{sql_cmd4}' \
                    f'{sql_cmd5}' \
                    f'select timenow();' \
                    f'{sql_cmd6}' \
                    f'select timenow();' \
                    f'select pg_sleep(35);' \
                    f'{sql_cmd8}' \
                    f'{sql_cmd9}'
        session2 = ComThread(self.pri_sh.execut_db_sql, args=(tras_sql2,))
        threads.append(session2)

        self.log.info('----启动线程----')
        thread_results = []
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join(180)
            thread_results.append(t.get_result())
        self.log.info('获取线程结果')
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG,
                      thread_results[0], '执行失败:' + step2_txt)
        self.assertIn('UPDATE 1', thread_results[0], '执行失败:' + step3_txt)
        self.assertIn('2 | mmm', thread_results[0].splitlines()[-9].strip(),
                      '执行失败:' + step3_txt)
        self.assertIn('2 | test', thread_results[1].splitlines()[7].strip(),
                      '执行失败:' + step4_txt)
        self.assertIsNotNone(thread_results[0].splitlines()[8].strip(),
                             '执行失败:' + step5_txt)
        self.log.info('分别获取step6中更新前及更新成功后的时间')
        start_time = thread_results[1].splitlines()[-16].strip()[:-3]
        self.log.info(start_time)
        trans_to_dtime1 = datetime.datetime.strptime(start_time,
                                                     '%Y-%m-%d %H:%M:%S')
        end_time = thread_results[1].splitlines()[-10].strip()[:-3]
        self.log.info(end_time)
        trans_to_dtime2 = datetime.datetime.strptime(end_time,
                                                     '%Y-%m-%d %H:%M:%S')
        self.log.info('计算会话2中加锁执行成功的阻塞时间')
        time_diff = trans_to_dtime2 - trans_to_dtime1
        self.log.info(time_diff)
        num = str(time_diff).split(':')[-1]
        self.log.info(f'阻塞时间为{num}')
        self.assertGreaterEqual(f'{num}', '02', '执行失败:' + step6_txt)
        self.assertTrue(self.constant.COMMIT_SUCCESS_MSG in thread_results[0],
                        '执行失败:' + step7_txt)
        self.assertTrue(self.constant.COMMIT_SUCCESS_MSG in thread_results[1],
                        '执行失败:' + step8_txt)

    def tearDown(self):
        text = '---step10:清理环境;expect:清理环境完成---'
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
            'Axls_Case0002 finish-')
