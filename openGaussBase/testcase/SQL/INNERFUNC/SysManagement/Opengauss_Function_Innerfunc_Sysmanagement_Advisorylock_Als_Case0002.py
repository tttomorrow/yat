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
Case Name   : pg_advisory_lock_shared(key1 int, key2 int)尝试获取会话级共享
             咨询锁
Description :
    1.创建表,使用一个唯一ID(用于advisory lock)插入数据
    2.会话1，更新表1的同时，使用advisory lock锁住这个ID,查询数据
    3.会话2对表2也进行加锁，查询，修改
    4.会话1提交事务
    5.会话2再次查询
    6.会话2提交事务
    7.清理环境
Expect      :
    1.创建成功;数据插入成功
    2.加锁成功，返回空；表1数据更新成功
    3.在会话1未提交事务之前，会话2加锁成功，表1查询到的是未更新的数据，
    在会话1提交后，会话2更新数据查到的是更新后的两个表数据
    4.提交成功
    5.会话2查询到了更新后的数据
    6.提交成功
    7.清理环境完成
"""

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
            'Case0002 start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = 'tb_advisorylock_als_0002'
        self.tb_name_01 = 'tb_advisorylock_als_0002_01'

    def test_advisorylock(self):
        step1_txt = '---step1:创建表,使用一个唯一ID(用于advisory lock),' \
                    '插入数据;expect:创建成功;数据插入成功---'
        self.log.info(step1_txt)
        sql_cmd1 = f"drop table if exists {self.tb_name};" \
                   f"create table {self.tb_name}" \
                   f"(id int4 primary key, info text);" \
                   f"insert into {self.tb_name} values (2,'test');" \
                   f"create table {self.tb_name_01}" \
                   f"(id int4 primary key, info text);" \
                   f"insert into {self.tb_name_01} values (2,'test');"

        step2_txt = '---step2:会话1，更新表1的同时，使用advisory lock' \
                    '锁住这个ID，查询数据;expect:加锁成功，表1数据更新成功---'
        self.log.info(step2_txt)
        sql_cmd2 = f"start transaction;" \
                   f"select pg_advisory_lock_shared(id, id) from " \
                   f"{self.tb_name};" \
                   f"update {self.tb_name} set info='mmm' where id=2;" \
                   f"select * from {self.tb_name} where id=2;"

        step3_txt = '---step3:会话2对表2也进行加锁，查询,修改;' \
                    'expect:在会话1未提交事务之前，会话2加锁成功，' \
                    '表1查询到的是未更新的数据，在会话1提交后，' \
                    '会话2更新数据查到的是更新后的两个表数据---'
        self.log.info(step3_txt)
        sql_cmd3 = f"start transaction;" \
                   f"select pg_advisory_lock_shared(id, id) from " \
                   f"{self.tb_name_01};" \
                   f"select * from {self.tb_name} where id=2;" \
                   f"update {self.tb_name_01} set info='ABC' where id=2;" \
                   f"select * from {self.tb_name_01} where id=2;"

        step4_txt = '--step4:会话1提交事务;expect:提交成功--'
        self.log.info(step4_txt)
        sql_cmd4 = "commit;"

        step5_txt = '--step5:会话2再次查询;expect:会话2查询到了更新后的数据--'
        self.log.info(step5_txt)
        sql_cmd5 = f"select * from {self.tb_name} where id=2;" \
                   f"select * from {self.tb_name_01} where id=2;"

        step6_txt = '--step6:会话2提交事务;expect:提交成功--'
        self.log.info(step6_txt)
        sql_cmd6 = "commit;"

        threads = []
        self.log.info('----线程1操作事务1:step1->step2->step4--')
        tras_sql1 = f'{sql_cmd1}' \
                    f'{sql_cmd2}' \
                    f'select pg_sleep(45);' \
                    f'{sql_cmd4}'
        session1 = ComThread(self.pri_sh.execut_db_sql, args=(tras_sql1,))
        threads.append(session1)

        self.log.info('----线程2操作事务2:step3->step5->step6---')
        tras_sql2 = f'select pg_sleep(40);' \
                    f'{sql_cmd3}' \
                    f'select pg_sleep(5);' \
                    f'{sql_cmd5}' \
                    f'{sql_cmd6}'
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
        msg1 = thread_results[0].splitlines()
        self.log.info(msg1)
        msg2 = thread_results[1].splitlines()
        self.log.info(msg2)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertTrue(
            thread_results[0].count(self.constant.INSERT_SUCCESS_MSG) == 2,
            '执行失败:' + step1_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG,
                      thread_results[0], '执行失败:' + step2_txt)
        self.assertIn('2 | mmm', thread_results[0],
                      '执行失败:' + step2_txt)
        self.assertIn('2 | test', thread_results[1], '执行失败:' + step3_txt)
        self.assertIn('UPDATE 1', thread_results[1], '执行失败:' + step3_txt)
        self.assertEqual('2 | ABC',
                         thread_results[1].splitlines()[-19].strip(),
                         '执行失败:' + step3_txt)
        self.assertEqual(self.constant.COMMIT_SUCCESS_MSG,
                         thread_results[0].splitlines()[-1].strip(),
                         '执行失败:' + step4_txt)
        self.assertIn('2 | ABC', thread_results[1],
                      '执行失败:' + step5_txt)
        self.assertEqual(self.constant.COMMIT_SUCCESS_MSG,
                         thread_results[1].splitlines()[-1].strip(),
                         '执行失败:' + step6_txt)

    def tearDown(self):
        text = '---step7:清理环境;expect:清理环境完成---'
        self.log.info(text)
        self.log.info('删除表')
        drop_msg = self.pri_sh.execut_db_sql(f"drop table if exists "
                                             f"{self.tb_name};"
                                             f"drop table if exists "
                                             f"{self.tb_name_01}")
        self.log.info(drop_msg)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Innerfunc_Sysmanagement_Advisorylock_'
            'Als_Case0002 finish-')
