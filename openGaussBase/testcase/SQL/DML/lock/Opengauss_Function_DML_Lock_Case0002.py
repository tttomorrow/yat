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
Case Type   : DML
Case Name   : 多个事务对同一张表上锁是否可以成功
Description :
    1.创建测试表
    2.在session1中开启事务，为测试表加share row exclusive锁
    3.在session2中开启事务，对测试表加share update exclusive锁
    4.查看视图pg_locks，查看share row exclusive锁是否添加成功
    5.清理环境
Expect      :
    1.创建测试表成功
    2.在session1中开启事务，为测试表加share row exclusive锁成功
    3.在session2中开启事务，对测试表加share update exclusive锁失败
    4.查看视图pg_locks，查看share row exclusive锁是否添加成功
    5.清理环境
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DmlTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_DML_Lock_Case0002开始')
        self.constant = Constant()
        self.commonsh1 = CommonSH('PrimaryDbUser')
        self.commonsh2 = CommonSH('PrimaryDbUser')

    def test_dml_lock(self):
        text1 = '-----step1: 创建测试表; expect: 创建成功-----'
        self.log.info(text1)
        sql_cmd = self.commonsh1.execut_db_sql(
            'drop table if exists t_lock_0002;'
            'create table t_lock_0002(sk integer,id char(16),'
            'name varchar(20),sq_ft integer);')
        self.log.info(sql_cmd)
        assert_in_1 = self.constant.CREATE_TABLE_SUCCESS in sql_cmd
        self.assertTrue(assert_in_1, '执行失败:' + text1)

        text2 = '-----step2: 在session1中开启事务，为测试表加share row ' \
                'exclusive锁，待session2开启事务后session1中执行step4; expect: 成功-----'
        self.log.info(text2)
        sql = '''start transaction;
            lock table t_lock_0002 in share row exclusive mode;
            
            --step4: 查看视图pg_locks，查看share row exclusive锁是否添加成功
            select pg_sleep(3); 
            select locktype,database,relation,transactionid,classid,\
            virtualtransaction,pid,sessionid,mode,\
            granted,fastpath from pg_locks;  
            '''
        thread_1 = ComThread(self.commonsh1.execut_db_sql, args=(sql, ''))
        thread_1.setDaemon(True)
        thread_1.start()

        text3 = '-----step3: 在session2中开启事务，对测试表加share update ' \
                'exclusive锁，待session1提交commit后session2再提交commit;' \
                ' expect: 加锁失败-----'
        self.log.info(text3)
        sql = '''select pg_sleep(1); 
            start transaction;
            lock table t_lock_0002 in share update exclusive mode;
            select pg_sleep(10);            
            '''
        thread_2 = ComThread(self.commonsh2.execut_db_sql, args=(sql, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        time.sleep(30)

        thread_1.join(1)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)

        thread_2.join(1)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)

        assert_eq_1 = msg_result_1.count('START TRANSACTION') is 1
        assert_eq_2 = msg_result_1.count('LOCK TABLE') is 1
        assert_eq_3 = msg_result_2.count('START TRANSACTION') is 1
        assert_eq_4 = msg_result_2.count('LOCK TABLE') is 1
        assert_in_1 = 'ShareRowExclusiveLock    | t' in msg_result_1
        assert_in_2 = 'ShareUpdateExclusiveLock | f' in msg_result_1
        self.assertTrue(assert_eq_1 and assert_eq_2 and assert_in_1
                        and assert_in_2,
                        '执行失败:' + text2)
        self.assertTrue(assert_eq_3 and assert_eq_4,
                        '执行失败:' + text3)

    def tearDown(self):
        text = '--step5: 清理环境; expect: 成功--'
        self.log.info(text)
        sql_cmd = self.commonsh1.execut_db_sql(f'drop table t_lock_0002;')
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_DML_Lock_Case0002结束')
