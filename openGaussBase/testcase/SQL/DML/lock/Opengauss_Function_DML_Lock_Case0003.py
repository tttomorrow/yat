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
Case Name   : 同一表是否可以获得两个事务的共享锁
Description :
    1.创建测试表
    2.开启事务，为测试表加share锁，不做commit操作
    3.开启新的session,在新的session中开启事务，再次对该测试表加share锁
    4.查看视图PG_LOCKS，查看锁是否都添加成功
    5.清理环境
Expect      :
    1.创建测试表成功
    2.开启事务，为测试表加share锁，不做commit操作
    3.开启新的session,在新的session中开启事务，再次对该测试表加share锁成功
    4.查看视图PG_LOCKS，查看锁都添加成功
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
        self.log.info('Opengauss_Function_DML_Lock_Case0003开始')
        self.constant = Constant()
        self.commonsh1 = CommonSH('PrimaryDbUser')
        self.t_name = 't_lock_0003'

    def test_dml_lock(self):
        text1 = '-----step1: 创建测试表; expect: 创建成功-----'
        self.log.info(text1)
        sql_cmd = self.commonsh1.execut_db_sql(
            f'drop table if exists {self.t_name};'
            f'create table {self.t_name}(sk integer,id char(16),'
            f'name varchar(20),sq_ft integer);')
        self.log.info(sql_cmd)
        assert_in_1 = self.constant.CREATE_TABLE_SUCCESS in sql_cmd
        self.assertTrue(assert_in_1, '执行失败:' + text1)

        text2 = '-----step2: 开启事务，为测试表加share锁，不做commit操作,成功' \
                '新session执行完step3后，在session1中执行step4; expect: 创建成功-----'
        self.log.info(text2)
        sql = f'''start transaction;
            lock table {self.t_name} in share mode;
            select pg_sleep(5);
            
            --step4: 查看视图pg_locks，查看锁是否都添加成功;expect: 加锁成功
             select mode from pg_locks where relation = \
             (select oid from pg_class where relname = '{self.t_name}');
            '''
        thread_1 = ComThread(self.commonsh1.execut_db_sql, args=(sql, ''))
        thread_1.setDaemon(True)
        thread_1.start()

        text3 = '----step3: 开启新的session,在新的session中开启事务，' \
                '再次对该测试表加share锁; expect: 加锁成功----'
        self.log.info(text3)
        sql = f'''select pg_sleep(1);
            start transaction;
            lock table {self.t_name} in share mode;
            select pg_sleep(6);
            '''
        thread_2 = ComThread(self.commonsh1.execut_db_sql, args=(sql, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        time.sleep(10)

        thread_1.join(1)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)

        thread_2.join(1)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)

        assert_eq_1 = msg_result_1.count('START TRANSACTION') is 1
        assert_eq_2 = msg_result_1.count('LOCK TABLE') is 1
        assert_eq_3 = msg_result_1.count('ShareLock') is 2
        self.assertTrue(assert_eq_1 and assert_eq_2 and assert_eq_3,
                        '执行失败:' + text2)
        assert_eq_4 = msg_result_2.count('START TRANSACTION') is 1
        assert_eq_5 = msg_result_2.count('LOCK TABLE') is 1
        self.assertTrue(assert_eq_4 and assert_eq_5,
                        '执行失败:' + text3)

    def tearDown(self):
        text = '--step5: 清理环境; expect: 清理成功--'
        self.log.info(text)
        sql_cmd = self.commonsh1.execut_db_sql(f'drop table t_lock_0003;')
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_DML_Lock_Case0003结束')
