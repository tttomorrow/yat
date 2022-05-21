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
Case Name   : 模拟死锁场景，统计函数结果transactionid事件failed_wait字段增加
Description :
    1、设置锁相关参数
    2、创建测试表并插入数据
    3、进行锁失败场景模拟前，查询fail_wait
    3、进行锁失败场景模拟前，查询死锁次数
    4、以线程开启事务，不同时间时序对表进行update操作
    5、开启新的事务，不同时间时序对表进行update操作
    6、进行锁失败场景后，查询fail_wait参数结果
    6、进行锁失败场景后，查看死锁次数
    7、相关视图结果验证
Expect      :
    1、设置锁相关参数，expect: 成功
    2、创建测试表并插入数据，expect: 创建成功
    3、进行锁失败场景模拟前，查询fail_wait，expect: 查询结果大于等于0
    3、进行锁失败场景模拟前，查询死锁次数，expect: 查询结果大于等于0
    4、以线程开启事务，不同时间时序对表进行update操作，expect: 操作成功
    5、开启新的事务，不同时间时序对表进行update操作，expect: 产生死锁
    6、进行锁失败场景后，查询fail_wait参数结果，expect: 较step3增加1
    6、查看死锁次数，expect: 较step3增加1
    7、相关视图结果验证，expect: 所有相关视图查询结果一致
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class DbeperfLock0003(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Dbeperf_Lock_Case0003:初始化----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.t_name1 = 't_dbeperf_lock0003_1'
        self.t_name2 = 't_dbeperf_lock0003_2'
        self.err_flag = 'ERROR:  deadlock detected'
        # 初始fail_wait值
        self.fail_wait0 = 0
        # 锁等待失败后，fail_wait值
        self.fail_wait1 = 1
        # 初始死锁值
        self.dead_num0 = 0
        # 锁等待失败后，死锁值
        self.dead_num1 = 1
        self.log.info('----查询数据库oid----')
        oid_cmd = f'select oid from PG_DATABASE where datname =' \
            f'\'{self.pri_dbuser.db_name}\';'
        oid_result = self.pri_sh.execut_db_sql(oid_cmd)
        self.oid = oid_result.strip().splitlines()[-2]

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
        create_sql = f'drop table if exists {self.t_name1};' \
            f'drop table if exists test2;' \
            f'create table {self.t_name1}(id int,name text);' \
            f'insert into {self.t_name1} values(1,\'test1\');' \
            f'create table {self.t_name2}(id int,name text);' \
            f'insert into {self.t_name2} values(1,\'test2\');'
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        suc_flag = create_result.count('INSERT 0 1')
        self.assertEqual(suc_flag, 2, '执行失败:' + step_txt)

        step_txt = '----step3: 进行锁失败场景模拟前，查询fail_wait，expect: 查询结果大于等于0---'
        self.log.info(step_txt)
        select_sql = 'select failed_wait from get_instr_wait_event(0) ' \
                     'where failed_wait>0 and event = \'transactionid\'; '
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        if '0 rows' in select_result:
            self.fail_wait0 = 0
        else:
            self.fail_wait0 = int(select_result.strip().splitlines()[-2])
        self.assertTrue(self.fail_wait0 >= 0, '执行失败:' + step_txt)

        step_txt = '----step3: 进行锁失败场景模拟前,查询死锁次数，expect: 查询结果大于等于0---'
        self.log.info(step_txt)
        dead_cmd = f'select * from pg_stat_get_db_deadlocks({self.oid})'
        dead_result = self.pri_sh.execut_db_sql(dead_cmd)
        self.log.info(dead_result)
        if '0 rows' in dead_result:
            self.dead_num0 = 0
        else:
            self.dead_num0 = int(dead_result.strip().splitlines()[-2])
        self.assertTrue(self.dead_num0 >= 0, '执行失败:' + step_txt)

        step4_txt = '----step4: 以线程开启事务，不同时间时序对表进行update操作，expect: 操作成功---'
        self.log.info(step4_txt)
        lock_sql1 = f'start transaction;' \
            f'update {self.t_name1}  set name=\'test11\' where id =1;' \
            f'select pg_sleep(10);' \
            f'update {self.t_name2} set name=\'test22\' where id =1;' \
            f'select pg_sleep(10);' \
            f'end;'
        session1 = ComThread(self.pri_sh.execut_db_sql, args=(lock_sql1,))
        session1.setDaemon(True)
        session1.start()
        time.sleep(5)

        step_txt = '----step5: 开启新的事务，不同时间时序对表进行update操作，expect: 产生死锁---'
        self.log.info(step_txt)
        lock_sql2 = f'start transaction;' \
            f'update {self.t_name2} set name=\'test22\' where id =1;' \
            f'select pg_sleep(7);' \
            f'update {self.t_name1} set name=\'test11\' where id =1;'
        lock_result = self.pri_sh.execut_db_sql(lock_sql2)
        self.log.info(lock_result)
        self.assertIn(self.err_flag, lock_result, '执行失败:' + step_txt)

        self.log.info("----session1事务执行结果----")
        session1.join()
        session1_result = session1.get_result()
        self.log.info(session1_result)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, session1_result,
                      '执行失败:' + step4_txt)

        step_txt = '----step6: 进行锁失败场景后，查询fail_wait参数结果，expect: 较step3增加1---'
        self.log.info(step_txt)
        select_sql = 'select failed_wait from get_instr_wait_event(0) ' \
                     'where failed_wait>0 and event = \'transactionid\'; '
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        self.fail_wait1 = int(select_result.strip().splitlines()[-2])
        self.assertTrue(self.fail_wait1 - self.fail_wait0 == 1,
                        '执行失败:' + step_txt)

        step_txt = '----step6: 查看死锁次数，expect: 较step3增加1---'
        self.log.info(step_txt)
        dead_cmd = f'select * from pg_stat_get_db_deadlocks({self.oid})'
        dead_result = self.pri_sh.execut_db_sql(dead_cmd)
        self.log.info(dead_result)
        self.dead_num1 = int(dead_result.strip().splitlines()[-2])
        self.assertTrue(self.dead_num1 - self.dead_num0 == 1,
                        '执行失败:' + step_txt)

        step_txt = '----step7: 相关视图结果验证，expect: 所有相关视图查询结果一致---'
        self.log.info(step_txt)
        select_sql = 'select * from get_instr_wait_event(0) ' \
                     'where failed_wait>0 and event = \'transactionid\'; '
        select_result1 = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result1)
        select_sql = 'select * from dbe_perf.wait_events where ' \
                     'failed_wait>0 and event = \'transactionid\';'
        select_result2 = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result2)
        select_sql = 'select * from dbe_perf.global_wait_events where ' \
                     'failed_wait>0 and event = \'transactionid\';'
        select_result3 = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result3)
        self.assertTrue(select_result1 == select_result2 == select_result3,
                        '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step8: 清除表数据----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t_name1};' \
            f'drop table if exists {self.t_name2};'
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)

        step_txt = '----step9: 还原参数----'
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

        self.log.info('----Opengauss_Function_Dbeperf_Lock_Case0003:执行完毕----')
