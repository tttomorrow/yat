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
Case Name   : pg_try_advisory_lock_shared(key bigint)尝试获取会话级共享咨询锁
Description :
    1.创建表,插入数据
    2.会话1，更新这条记录的同时，使用advisory lock锁住这个ID，查询数据
    3.会话2，查询,执行更新数据语句
    4.会话1提交事务
    5.会话2再次查询
    6.会话1执行更新动作并加锁
    7.会话2查询这条记录时，使用advisory lock探测这条记录
    8.清理环境
Expect      :
    1.创建成功;数据插入成功
    2.加锁成功，数据更新成功,返回t
    3.查询到的是未更新过的数据，更新语句处于等待状态
    4.提交成功
    5.会话1提交事务后,会话2中查询到了自己更新后的数据
    6.加锁成功返回t，查询到数据更新成功
    7.会话2查询的数据是已经更新过的
    8.清理环境完成
              避免执行sql语句时间执行顺序变化，导致断言失败
              session2数据未更新
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
        self.tb_name = 'tb_advisorylock_tals_case0001'

    def test_advisorylock(self):
        step1_txt = '---step1:创建表,插入数据;expect:创建成功;数据插入成功---'
        self.log.info(step1_txt)
        sql_cmd1 = f"drop table if exists {self.tb_name};" \
                   f"create table {self.tb_name}(id int8 primary key, " \
                   f"info text);" \
                   f"insert into {self.tb_name} values(1, 'test');"

        step2_txt = '---step2:会话1，更新这条记录的同时，使用advisory lock' \
                    '锁住这个ID，查询数据;expect:加锁成功，数据更新成功,返回t-'
        self.log.info(step2_txt)
        sql_cmd2 = f"start transaction;" \
                   f"update {self.tb_name} set info='abc' where id=1 " \
                   f"returning pg_try_advisory_lock_shared(id);" \
                   f"select * from {self.tb_name} where id=1;"

        step3_txt = '---step3:会话2，查询,执行更新数据语句;' \
                    'expect:查询到的是未更新过的数据，更新语句处于等待状态--;'
        self.log.info(step3_txt)
        sql_cmd3 = f"select * from {self.tb_name};" \
                   f"update {self.tb_name} set info='hhh' where id=1 " \
                   f"returning pg_try_advisory_lock_shared(id);"

        step4_txt = '--step4:会话1提交事务;expect:提交成功--'
        self.log.info(step4_txt)
        sql_cmd4 = "commit;"

        step5_txt = '--step5:会话2再次查询;expect:会话1提交事务后，' \
                    '会话2中查询到了自己更新后的数据--'
        self.log.info(step5_txt)
        sql_cmd5 = f"select * from {self.tb_name} where id =1;"

        step6_txt = '--step6:会话1执行更新动作并加锁;' \
                    'expect:加锁成功返回t，查询到数据更新成功--'
        self.log.info(step6_txt)
        sql_cmd6 = f"update {self.tb_name} set info='abc' where id=1 " \
                   f"returning pg_try_advisory_lock_shared(id);"

        step7_txt = '---step7:会话2查询这条记录时，使用advisory lock探测这' \
                    '条记录;expect:会话2查询的数据是已经更新过的---'
        self.log.info(step7_txt)
        sql_cmd7 = f" select * from {self.tb_name} where id=1 and " \
                   f"pg_try_advisory_lock_shared(id);"

        threads = []
        self.log.info('----线程1操作事务1:step1->step2->step4->step6--')
        tras_sql1 = f'{sql_cmd1}' \
                    f'{sql_cmd2}' \
                    f'select pg_sleep(20);' \
                    f'{sql_cmd4}' \
                    f'select pg_sleep(30);' \
                    f'{sql_cmd6};'
        session1 = ComThread(self.pri_sh.execut_db_sql, args=(tras_sql1,))
        threads.append(session1)

        self.log.info('----线程2操作事务2:step3->step5->step7----')
        tras_sql2 = f'select pg_sleep(15);' \
                    f'select timenow();' \
                    f'{sql_cmd3}' \
                    f'select timenow();' \
                    f'select pg_sleep(20);' \
                    f'{sql_cmd5}' \
                    f'select pg_sleep(35);' \
                    f'{sql_cmd7}'
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
        self.log.info('获取线程结果')
        msg1 = thread_results[0].splitlines()
        self.log.info(msg1)
        msg2 = thread_results[1].splitlines()
        self.log.info(msg2)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertIn('1 | abc', thread_results[0].splitlines()[14].strip(),
                      '执行失败:' + step2_txt)
        self.assertIn('1 | test', thread_results[1].splitlines()[12].strip(),
                      '执行失败:' + step3_txt)
        self.assertIn('COMMIT', thread_results[0].splitlines()[-12].strip(),
                      '执行失败:' + step4_txt)
        self.assertIn('1 | hhh', thread_results[1].splitlines()[-12].strip(),
                      '执行失败:' + step5_txt)
        self.assertIn('UPDATE 1', thread_results[0].splitlines()[-1].strip(),
                      '执行失败:' + step6_txt)
        self.assertIn('1 | abc', thread_results[1].splitlines()[-2].strip(),
                      '执行失败:' + step7_txt)

    def tearDown(self):
        text = '---step8:清理环境;expect:清理环境完成---'
        self.log.info(text)
        self.log.info('删除表')
        drop_msg = self.pri_sh.execut_db_sql(f"drop table if exists "
                                             f"{self.tb_name};")
        self.log.info(drop_msg)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
