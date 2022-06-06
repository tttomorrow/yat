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
Case Type   : DML-NEW-LOCK
Case Name   : 验证for key share与for key share无阻塞
Description :
    1.建表 插入数据;expect:成功
    2.会话1开启事务暂不提交 执行for key share;expect:成功
    3.会话2 分别开启以下事务 执行for key share;expect:成功 不阻塞
    --child里insert数据会获取parent的key share;expect:成功 不阻塞
    --child里update数据关联键会获取parent的key share;expect:成功 不阻塞
    --child里第二次update数据非关联键会获取parent的key share;expect:成功 不阻塞
    4.执行commit并清理环境;expect:成功
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
History     :
"""
import os
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class USTORE(unittest.TestCase):

    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.log = Logger()
        self.table1 = 't_lock_0120_01'
        self.table2 = 't_lock_0120_02'
        text = f'---{os.path.basename(__file__)} start---'
        self.log.info(text)

    def testunit_1(self):
        text = '--step1:建表 插入数据;expect:成功--'
        self.log.info(text)
        sql = f'''drop table if exists {self.table1} cascade;
        drop table if exists {self.table2} cascade;
        create table {self.table1}(c_int1 int primary key, c_int2 int);
        create table {self.table2}(c_int3 int , c_int4 int);
        insert into {self.table1} values (generate_series(1,20), 
        generate_series(1,20));
        insert into {self.table2} values (generate_series(1,20), 
        generate_series(1,20));
        alter table {self.table2} add foreign key (c_int3) references 
        {self.table1} (c_int1);
        '''
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result,
                      '执行失败: ' + text)

        text = '--step2:会话1开启事务暂不提交 执行for key share;expect:成功--'
        self.log.info(text)
        sql = f'''start transaction;
                select c_int2 from {self.table1} where c_int1 = 3 
                for key share;
                select mode from pg_lock_status() where relation 
                in (select oid from pg_class where relname='{self.table1}');
                select mode from pg_locks where relation in 
                (select oid from pg_class where relname='{self.table1}');
                select mode from dbe_perf.locks where relation in 
                (select oid from pg_class where relname='{self.table1}');
                select mode from dbe_perf.global_locks where relation in 
                (select oid from pg_class where relname='{self.table1}');
                select pg_sleep(120);
                commit;
            '''
        test_thread = ComThread(self.pri_sh.execut_db_sql, args=(sql,))
        test_thread.setDaemon(True)

        test_sql1 = f'''--执行for key share;
        start transaction;
            select c_int2 from {self.table1} where c_int1 = 3 for key share;
            select mode from pg_lock_status() where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from pg_locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from dbe_perf.locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from dbe_perf.global_locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
        commit;
        '''
        test_sql2 = f'''--child里insert数据会获取parent的key;
        start transaction;
            insert into {self.table2} values(1, 1);
            select mode from pg_lock_status() where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from pg_locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from dbe_perf.locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from dbe_perf.global_locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
        commit;
        '''
        test_sql3 = f'''--child里update数据关联键会获取parent的key share;
        truncate t_lock_0120_02;
        insert into t_lock_0120_02 values(1, 1);
        start transaction;
        update t_lock_0120_02 set c_int4=2 where c_int3=1;
        update t_lock_0120_02 set c_int4=3 where c_int3=1;
        select mode from pg_lock_status() where relation in 
        (select oid from pg_class where relname='t_lock_0120_01');
        select mode from pg_locks where relation in 
        (select oid from pg_class where relname='t_lock_0120_01');
        select mode from dbe_perf.locks where relation in 
        (select oid from pg_class where relname='t_lock_0120_01');
        select mode from dbe_perf.global_locks where relation in 
        (select oid from pg_class where relname='t_lock_0120_01');
        commit;

        '''
        test_sql4 = f'''--child里第二次update数据非关联键会获取parent的key share;
        truncate {self.table2};
        insert into {self.table2} values(1, 1);
        start transaction;
            update {self.table2} set c_int4=2 where c_int3=3;
            update {self.table2} set c_int4=3 where c_int3=3;
            select mode from pg_lock_status() where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from pg_locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from dbe_perf.locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from dbe_perf.global_locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
        commit;
        '''

        test_thread.start()
        time.sleep(2)
        text = '--step3:会话2 分别开启以下事务 执行for key share;expect:成功--'
        self.log.info(text)
        sql_list = [test_sql1, test_sql2, test_sql3, test_sql4]
        for sql in sql_list:
            self.log.info(sql)
            update_thread = ComThread(self.pri_sh.execut_db_sql,
                                      args=(sql,))
            update_thread.setDaemon(True)
            update_thread.start()

            update_thread.join(60)
            result = update_thread.get_result()
            self.log.info('result:' + str(sql_list.index(sql)))
            self.log.info(result)
            self.assertNotIn('ERROR', result, '执行失败: ' + text)
            self.assertIn('RowShareLock', result, '执行失败: ' + text)

        self.log.info("会话1线程执行结果")
        test_thread.join(130)
        result = test_thread.get_result()
        self.log.info(result)
        self.assertNotIn('ERROR', result, '执行失败: ' + text)

    def tearDown(self):
        text = '--step4:清理环境;expect:成功--'
        self.log.info(text)
        sql = f'drop table {self.table1},{self.table2} cascade;'
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, result,
                      '执行失败: ' + text)
        text = f'---{os.path.basename(__file__)} end---'
        self.log.info(text)
