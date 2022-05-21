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
            '-Opengauss_Function_Innerfunc_Sysmanagement_Advisorylock_Tal_'
            'Case0001 start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = 'tb_advisorylock_tal_case0001'

    def test_advisorylock(self):
        step1_txt = '---step1:创建表,插入数据;expect:创建成功;数据插入成功---'
        self.log.info(step1_txt)
        sql_cmd = f"drop table if exists {self.tb_name};" \
                  f"create table {self.tb_name}(id int8 primary key, " \
                  f"info text);" \
                  f"insert into {self.tb_name} values(1, 'test');"
        execute_cmd = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(execute_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, execute_cmd,
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, execute_cmd,
                      '执行失败:' + step1_txt)

        step2_txt = '会话1执行以下操作'
        self.log.info(step2_txt)
        self.log.info('---step2.1:会话1,更新某一条记录;expect:数据更新成功---')
        self.log.info('--step2.2:会话1，先commit上个事务;expect:提交成功--')
        self.log.info('--step2.3:会话1，然后更新这条记录的同时,使用advisory'
                      'lock锁住这个ID;expect:加锁成功--')
        self.log.info('--step2.4:会话1提交事务;expect:提交事务成功')
        sql_cmd = f"start transaction;" \
                  f"update {self.tb_name} set info='abc' where id=1;" \
                  f"select pg_sleep(15);" \
                  f"commit;" \
                  f"start transaction;" \
                  f"update {self.tb_name} set info='abc' where id=1 " \
                  f"returning pg_try_advisory_lock(id);" \
                  f"select pg_sleep(30);" \
                  f"commit;"
        thread_1 = ComThread(self.pri_sh.execut_db_sql, args=(sql_cmd, ''))
        thread_1.setDaemon(True)
        thread_1.start()

        step3_txt = '会话2执行以下操作'
        self.log.info(step3_txt)
        self.log.info('---step3.1:会话2，读这条记录;expect:读写不冲突，'
                      '查询成功;数据未更新---')
        self.log.info('--step3.2:会话2，查询这条记录时，使用advisory lock探测'
                      '这条记录;expect:加锁的行不能再读，查到0行--')
        self.log.info('--step3.3:会话1关闭，会话2再次查询;'
                      'expect:会话1关闭后会话2查询到1行--')

        sql_cmd = f"select pg_sleep(11);" \
                  f"select * from {self.tb_name};" \
                  f"select pg_sleep(30);" \
                  f"select * from {self.tb_name} where id=1 and " \
                  f"pg_try_advisory_lock(1);" \
                  f"select pg_sleep(20);" \
                  f"select * from {self.tb_name} where id=1 and " \
                  f"pg_try_advisory_lock(1);"
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
        self.assertTrue(msg_result_1.count(
            self.constant.START_TRANSACTION_SUCCESS_MSG) == 2,
                        '执行失败:' + step2_txt)
        self.assertIn('UPDATE 1', msg_result_1, '执行失败:' + step2_txt)
        self.assertIn('1 | test', msg_result_2.splitlines()[7].strip(),
                      '执行失败:' + step3_txt)
        self.assertTrue(msg_result_1.count('COMMIT') == 2,
                        '执行失败:' + step2_txt)
        self.assertIn('t', msg_result_1, '执行失败:' + step2_txt)
        self.assertIn('(0 rows)', msg_result_2.splitlines()[-11].strip(),
                      '执行失败:' + step3_txt)
        self.assertIn('(1 row)', msg_result_2.splitlines()[-1].strip(),
                      '执行失败:' + step3_txt)

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
            'Tal_Case0001 finish-')
