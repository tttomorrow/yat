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
Case Type   : DBE_PERF功能类
Case Name   : 模拟事务ID锁场景，查询dbe_perf.GLOBAL_LOCKS视图，transactionID字段为相应事务ID
Description :
    1、设置锁相关参数
    2、创建测试表并插入数据
    3、以线程开启事务，对表进行update操作
    4、以线程开启事务，对表进行update操作
    5、查询GLOBAL_LOCKS视图
    6、相关视图结果验证
Expect      :
    1、设置锁相关参数，expect: 成功
    2、创建测试表并插入数据，expect: 创建成功
    3、以线程开启事务，对表进行update操作，expect: 操作成功
    4、以线程开启事务，对表进行update操作，expect: 操作失败
    5、查询GLOBAL_LOCKS视图，expect: transactionid非空
    6、相关视图结果验证，expect: 所有相关视图查询结果一致
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class DbeperfLock0004(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Dbeperf_Lock_Case0004:初始化----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.t_name = 't_dbeperf_lock0004'
        self.err_flag = 'ERROR:  Lock wait timeout'

    def test_main(self):
        self.log.info('----查询相关参数----')
        result = self.pri_sh.execut_db_sql(
            'show allow_concurrent_tuple_update;')
        self.log.info(f"allow_concurrent_tuple_update is {result}")
        self.para1 = result.strip().splitlines()[-2]

        result = self.pri_sh.execut_db_sql(
            'show update_lockwait_timeout;')
        self.log.info(f"update_lockwait_timeout is {result}")
        self.para2 = result.strip().splitlines()[-2]

        result = self.pri_sh.execut_db_sql(
            'show lockwait_timeout;')
        self.log.info(f"lockwait_timeout is {result}")
        self.para3 = result.strip().splitlines()[-2]

        step_txt = '----step1: 设置锁相关参数，expect: 成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           "allow_concurrent_tuple_update=on")
        self.assertTrue(result, '执行失败:' + step_txt)
        result = self.pri_sh.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           "update_lockwait_timeout = 30000")
        self.assertTrue(result, '执行失败:' + step_txt)
        result = self.pri_sh.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           "lockwait_timeout = 30000")
        self.assertTrue(result, '执行失败:' + step_txt)

        step_txt = '----step2: 创建测试表并插入数据，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.t_name};' \
            f'create table {self.t_name}(id int,name text);' \
            f'insert into {self.t_name} values(1,\'test1\');'
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn('INSERT 0 1', create_result, '执行失败:' + step_txt)

        step3_txt = '----step3: 以线程开启事务，对表进行update操作，expect: 操作成功---'
        self.log.info(step3_txt)
        lock_sql1 = f'start transaction;' \
            f'update {self.t_name} set name=\'test11\' where id =1;' \
            f'select pg_sleep(35);' \
            f'end;'
        session1 = ComThread(self.pri_sh.execut_db_sql, args=(lock_sql1,))
        session1.setDaemon(True)
        session1.start()
        time.sleep(4)

        step4_txt = '----step4: 以线程开启事务，对表进行update操作，expect: 操作失败---'
        self.log.info(step4_txt)
        lock_sql1 = f'start transaction;' \
            f'update {self.t_name} set name=\'test11\' where id =1;' \
            f'select pg_sleep(20);' \
            f'end;'
        session2 = ComThread(self.pri_sh.execut_db_sql, args=(lock_sql1,))
        session2.setDaemon(True)
        session2.start()
        time.sleep(5)

        step_txt = '----step5: 查询GLOBAL_LOCKS视图，expect: transactionid非空---'
        self.log.info(step_txt)
        select_sql1 = f'select transactionid from dbe_perf.GLOBAL_LOCKS ' \
            f'where locktype=\'transactionid\'; '
        select_result1 = self.pri_sh.execut_db_sql(select_sql1)
        self.log.info(select_result1)
        select_sql2 = f'select transactionid from dbe_perf.GLOBAL_LOCKS ' \
            f'where locktype=\'transactionid\' and transactionid is not null;'
        select_result2 = self.pri_sh.execut_db_sql(select_sql2)
        self.log.info(select_result2)
        self.assertEqual(select_result1, select_result2, '执行失败:' + step_txt)

        step_txt = '----step6: 相关视图结果验证，expect: 所有相关视图查询结果一致---'
        self.log.info(step_txt)
        select_sql = 'select locktype, transactionid, mode ' \
                     'from pg_lock_status() ' \
                     'where locktype=\'transactionid\'; '
        select_result1 = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result1)
        select_sql = 'select locktype, transactionid, mode ' \
                     'from dbe_perf.global_locks ' \
                     'where locktype=\'transactionid\';'
        select_result2 = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result2)
        select_sql = 'select locktype, transactionid, mode ' \
                     'from dbe_perf.locks ' \
                     'where locktype=\'transactionid\';'
        select_result3 = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result3)
        self.assertTrue(select_result1 == select_result2 == select_result3,
                        '执行失败:' + step_txt)

        self.log.info("----session1事务执行结果----")
        session1.join()
        session1_result = session1.get_result()
        self.log.info(session1_result)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, session1_result,
                      '执行失败:' + step3_txt)

        self.log.info("----session2事务执行结果----")
        session2.join()
        session2_result = session2.get_result()
        self.log.info(session2_result)
        self.assertIn(self.err_flag, session2_result,
                      '执行失败:' + step4_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step7: 清除表数据----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t_name};'
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)

        step_txt = '----step8: 还原参数----'
        self.log.info(step_txt)
        self.pri_sh.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"allow_concurrent_tuple_update = "
                                  f"{self.para1}")
        self.pri_sh.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"update_lockwait_timeout = {self.para2}")
        self.pri_sh.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"lockwait_timeout = {self.para3}")

        self.log.info('----Opengauss_Function_Dbeperf_Lock_Case0004:执行完毕----')
