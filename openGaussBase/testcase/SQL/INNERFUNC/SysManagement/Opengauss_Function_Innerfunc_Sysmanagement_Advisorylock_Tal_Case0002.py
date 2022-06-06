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
Case Name   : pg_try_advisory_lock(key bigint)尝试获取会话级排它咨询锁
Description :
    1.创建表,插入数据
    2.会话1,更新某一条记录
    3.会话2，读这条记录
    4.会话1，先commit上个事务
    5.会话1，然后更新这条记录的同时,使用advisory lock锁住这个ID
    6.会话2，查询这条记录时，使用advisory lock探测这条记录
    7.会话1提交事务
    8.会话1关闭，会话2再次查询
    9.清理环境
Expect      :
    1.创建成功;数据插入成功
    2.数据更新成功
    3.读写不冲突，查询成功;数据未更新
    4.提交成功
    5.加锁成功
    6.加锁的行不能再读，查到0行
    7.提交成功
    8.会话1关闭后会话2查询到1行
    9.清理环境完成
              避免执行sql语句时间执行顺序变化，导致断言失败
"""

import os
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Innerfunc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = 'tb_advisorylock_tal_case0002'

    def test_advisorylock(self):
        step1_txt = '---step1:创建表,插入数据;expect:创建成功;数据插入成功---'
        self.log.info(step1_txt)
        sql_cmd1 = f"drop table if exists {self.tb_name};" \
                   f"create table {self.tb_name}(id int4 primary key, " \
                   f"info text);" \
                   f"insert into {self.tb_name} values(1, 'test');"

        step2_txt = '---step2:会话1,更新某一条记录;expect:数据更新成功---'
        self.log.info(step2_txt)
        sql_cmd2 = f"start transaction;" \
                   f"update {self.tb_name} set info='abc' where id=1;"

        step3_txt = '---step3:会话2，读这条记录;expect:读写不冲突，查询成功;' \
                    '数据未更新---'
        self.log.info(step3_txt)
        sql_cmd3 = f"select * from {self.tb_name};"

        step4_txt = '--step4:会话1，先commit上个事务;expect:提交成功--'
        self.log.info(step4_txt)
        sql_cmd4 = "commit;"

        step5_txt = '--step5:会话1，然后更新这条记录的' \
                    '同时,使用advisory lock锁住这个ID;expect:加锁成功--'
        self.log.info(step5_txt)
        sql_cmd5 = f"start transaction;" \
                   f"update {self.tb_name} set info='abc' where id=1 " \
                   f"returning pg_try_advisory_lock(id,id);"

        step6_txt = '--step6:会话2，查询这条记录时，使用advisory lock探测' \
                    '这条记录;expect:加锁的行不能再读，查到0行--'
        self.log.info(step6_txt)
        sql_cmd6 = f"select * from {self.tb_name} where id=1 and " \
                   f"pg_try_advisory_lock(1,1);"

        step7_txt = '---step7:会话1提交事务;expect:提交事务成功---'
        self.log.info(step7_txt)
        sql_cmd7 = "commit;"

        step8_txt = '--step8:会话1关闭，会话2再次查询;' \
                    'expect:会话1关闭后会话2查询到1行--'
        self.log.info(step8_txt)
        sql_cmd8 = f"select * from {self.tb_name} where id=1 and " \
                   f"pg_try_advisory_lock(1,1);"

        threads = []
        self.log.info('----线程1操作事务1:step1->step2->step4->step5->step7--')
        tras_sql1 = f'{sql_cmd1}' \
                    f'{sql_cmd2}' \
                    f'select pg_sleep(20);' \
                    f'{sql_cmd4}' \
                    f'{sql_cmd5};' \
                    f'select pg_sleep(30);' \
                    f'{sql_cmd7}'
        session1 = ComThread(self.pri_sh.execut_db_sql, args=(tras_sql1,))
        threads.append(session1)

        self.log.info('----线程2操作事务2:step3->step6----')
        tras_sql2 = f'select pg_sleep(15);' \
                    f'{sql_cmd3}' \
                    f'select pg_sleep(30);' \
                    f'{sql_cmd6}' \
                    f'select pg_sleep(35);' \
                    f'{sql_cmd8}'
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
            self.log.info(t.get_result())
        msg = thread_results[0].splitlines()
        self.log.info(msg)
        msg = thread_results[1].splitlines()
        self.log.info(msg)
        self.log.info('获取线程结果')
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertTrue(thread_results[0].count(
            self.constant.START_TRANSACTION_SUCCESS_MSG) == 2,
                        '执行失败:' + step2_txt)
        self.assertIn('UPDATE', thread_results[0], '执行失败:' + step2_txt)
        self.assertIn('1 | test', thread_results[1].splitlines()[7].strip(),
                      '执行失败:' + step3_txt)
        self.assertTrue(thread_results[0].count('COMMIT') == 2,
                        '执行失败:' + step4_txt)
        self.assertIn('t', thread_results[0].splitlines()[-10].strip(),
                      '执行失败:' + step5_txt)
        self.assertIn('(0 rows)', thread_results[1].splitlines()[-11].strip(),
                      '执行失败:' + step6_txt)
        self.assertIn('(1 row)', thread_results[1].splitlines()[-1].strip(),
                      '执行失败:' + step8_txt)

    def tearDown(self):
        text = '---step9:清理环境;expect:清理环境完成---'
        self.log.info(text)
        self.log.info('删除表')
        drop_msg = self.pri_sh.execut_db_sql(f"drop table if exists "
                                             f"{self.tb_name};")
        self.log.info(drop_msg)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
