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
Case Name   : 验证for key share与for share无阻塞
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
import sys
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
        self.table1 = 't_lock_0121_01'
        self.table2 = 't_lock_0121_02'
        text = f'---{os.path.basename(sys.argv[0])} start---'
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
        alter table {self.table2} add foreign key (c_int3) 
        references {self.table1} (c_int1);
        '''
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result,
                      '执行失败: ' + text)

        text = '--step2:会话1分别开启事务暂不提交 执行for key share;expect:成功--'
        self.log.info(text)
        test_sql1 = f'''--执行for key share;
        start transaction;
            select c_int2 from {self.table1} where c_int1 = 3 
            for key share;
            select mode from pg_lock_status() where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from pg_locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from dbe_perf.locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select mode from dbe_perf.global_locks where relation in 
            (select oid from pg_class where relname='{self.table1}');
            select pg_sleep(60);
        commit;
            '''

        test_sql2 = f'''--执行for key share;
        start transaction;
            select c_int4 from {self.table2} where c_int3 = 3 for key share;
            select * from {self.table2} where c_int3 = 3 for key share;
            select mode from pg_lock_status() where relation in
            (select oid from pg_class where relname='{self.table2}');
            select mode from pg_locks where relation in
            (select oid from pg_class where relname='{self.table2}');
            select mode from dbe_perf.locks where relation in
            (select oid from pg_class where relname='{self.table2}');
            select mode from dbe_perf.global_locks where relation in
            (select oid from pg_class where relname='{self.table2}');
            select pg_sleep(60);
        commit;
        '''
        test_sql3 = f'''--child里insert数据会获取parent的key share;
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
            select pg_sleep(60);
        commit;
        '''
        test_sql4 = f'''--child里update数据关联键会获取parent的key share;
        update t_lock_0121_02 set c_int3=2 where c_int3 =1;
        select mode from pg_lock_status() where relation in 
        (select oid from pg_class where relname='t_lock_0121_01');
        select mode from pg_locks where relation in 
        (select oid from pg_class where relname='t_lock_0121_01');
        select mode from dbe_perf.locks where relation in 
        (select oid from pg_class where relname='t_lock_0121_01');
        select mode from dbe_perf.global_locks where relation in 
        (select oid from pg_class where relname='t_lock_0121_01');
        select pg_sleep(60);
        commit;
        '''
        test_sql5 = f'''--child里第二次update数据非关联键会获取parent的key share;
        truncate {self.table2};
        insert into {self.table2} values(1, 1);
        start transaction;
            update {self.table2} set c_int4=2 where c_int3 =1;
            update {self.table2} set c_int4=3 where c_int3 =1;
            select mode from pg_lock_status() where relation in
            (select oid from pg_class where relname='{self.table1}');
            select mode from pg_locks where relation in
            (select oid from pg_class where relname='{self.table1}');
            select mode from dbe_perf.locks where relation in
            (select oid from pg_class where relname='{self.table1}');
            select mode from dbe_perf.global_locks where relation in
            (select oid from pg_class where relname='{self.table1}');
            select pg_sleep(60);
        commit;
        '''
        sql_list = [test_sql1, test_sql2, test_sql3, test_sql4, test_sql5]
        thread_list = []
        for sql in sql_list:
            self.log.info(sql)
            test_thread = ComThread(self.pri_sh.execut_db_sql,
                                      args=(sql,))
            test_thread.setDaemon(True)
            thread_list.append(test_thread)

        text = '--step3:会话2 开启事务 执行for share;expect:成功--'
        self.log.info(text)
        sql = f'''start transaction;
            select c_int2 from {self.table1} where c_int1 = 3 for share;
            select c_int1,c_int2 from {self.table1} where c_int1 = 3 for share;
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
        forshare_thread = ComThread(self.pri_sh.execut_db_sql, args=(sql,))
        forshare_thread.setDaemon(True)

        for thread in thread_list:
            thread.start()
        forshare_thread.start()
        forshare_thread.join(30)
        result = forshare_thread.get_result()
        self.log.info(result)
        self.assertNotIn('ERROR', result, '执行失败: ' + text)
        self.assertIn('RowShareLock', result, '执行失败: ' + text)

        self.log.info("会话1线程执行结果")
        for thread in thread_list:
            thread.join(130)
            result = thread.get_result()
            self.log.info('result:' + str(thread_list.index(thread)))
            self.log.info(result)
            self.assertNotIn('ERROR', result, '执行失败: ' + text)
            self.assertIn('RowShareLock', result, '执行失败: ' + text)

    def tearDown(self):
        text = '--step4:清理环境;expect:成功--'
        self.log.info(text)
        sql = f'drop table {self.table1},{self.table2} cascade;'
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, result,
                      '执行失败: ' + text)
        text = f'---{os.path.basename(sys.argv[0])} end---'
        self.log.info(text)
