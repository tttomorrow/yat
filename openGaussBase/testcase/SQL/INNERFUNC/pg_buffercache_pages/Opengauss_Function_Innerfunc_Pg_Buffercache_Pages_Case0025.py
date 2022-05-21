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
Case Type   : pg_buffercache_pages函数功能
Case Name   : pg_buffercache_pages函数，多个会话开始事务不提交，进行同行数据更新，pinning_backends查询正确
Description :
    1.创建测试表并插入数据
    2.会话1开启事务，对表进行update操作，不进行提交
    3.会话2开启新的会话，执行相同表相同行数据操作
    4.会话3开启新的会话，执行相同表相同行数据操作
    5.步骤2、3、4 无返回的情况下，查询缓存信息
    6.会话1事务提交
    7.再次查询缓存信息
Expect      :
    1.建表插数据成功
    2.事务内update成功
    3.会话2启动相同update操作，新会话启动成功
    4.会话3启动相同update操作，新会话启动成功
    5.步骤2、3、4 无返回的情况下，查询缓存信息，pinning_backends数量查询为2
    6.会话1提交正常，其他会话更新成功
    7.pinning_backends数量查询为0
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class PgBuffercachePagesCase0025(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0025:初始化')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.t_name = 't_pg_buffercache_pages_case0025'

    def test_main(self):
        step_txt = '----step1: 创建测试表并插入数据，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.t_name};' \
            f'create table {self.t_name}(id int,name text);' \
            f'insert into {self.t_name} values(1,\'test1\');'
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn('INSERT 0 1', create_result, '执行失败:' + step_txt)

        step2_txt = '----step2:会话1开启事务，对表进行update操作，不进行提交 expect: 操作成功---'
        self.log.info(step2_txt)
        update_sql1 = f'start transaction;' \
            f'update {self.t_name} set name=\'test11\' where id =1;' \
            f'select pg_sleep(10);' \
            f'end;'
        session1 = ComThread(self.pri_sh.execut_db_sql, args=(update_sql1,))
        session1.setDaemon(True)
        session1.start()
        time.sleep(2)

        step3_txt = '----step3:会话2开启新的会话，执行相同表相同行数据操作 expect: 操作成功---'
        self.log.info(step3_txt)
        update_sql2 = f'start transaction;' \
            f'update {self.t_name} set name=\'test11\' where id =1;' \
            f'end;'
        session2 = ComThread(self.pri_sh.execut_db_sql, args=(update_sql2,))
        session2.setDaemon(True)
        session2.start()
        time.sleep(2)

        step4_txt = '----step4: 会话3开启新的会话，执行相同表相同行数据操作 expect: 操作成功---'
        self.log.info(step4_txt)
        update_sql3 = f'start transaction;' \
            f'update {self.t_name} set name=\'test11\' where id =1;' \
            f'end;'
        session3 = ComThread(self.pri_sh.execut_db_sql, args=(update_sql3,))
        session3.setDaemon(True)
        session3.start()
        time.sleep(2)

        step5_txt = '----step5: 步骤2、3、4 无返回的情况下，查询缓存信息，' \
                    'expect:pinning_backends数量查询为2---'
        self.log.info(step5_txt)
        select_sql = f'select pinning_backends from pg_buffercache_pages()' \
            f'where relfilenode in ' \
            f'(select oid from pg_class where relname=\'{self.t_name}\') ;'
        select_result1 = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result1)
        self.assertIn('2', select_result1, '执行失败:' + step5_txt)

        step6_txt = '----step6: 会话1提交正常，expect: 其他会话更新成功---'
        self.log.info(step6_txt)
        self.log.info("----session1事务执行结果----")
        session1.join()
        session1_result = session1.get_result()
        self.log.info(session1_result)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, session1_result,
                      '执行失败:' + step6_txt)
        self.log.info("----session2事务执行结果----")
        session2.join()
        session2_result = session2.get_result()
        self.log.info(session2_result)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, session2_result,
                      '执行失败:' + step6_txt)
        self.log.info("----session3事务执行结果----")
        session3.join()
        session3_result = session3.get_result()
        self.log.info(session3_result)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, session3_result,
                      '执行失败:' + step6_txt)

        step7_txt = '----step7: 再次查询缓存信息 expect: pinning_backends数量查询为0---'
        self.log.info(step7_txt)
        select_sql = f'select pinning_backends from pg_buffercache_pages()' \
            f'where relfilenode in ' \
            f'(select oid from pg_class where relname=\'{self.t_name}\') ;'
        select_result1 = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result1)
        self.assertIn('0', select_result1, '执行失败:' + step7_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step8: 清除表数据----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t_name};'
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0025:执行完毕')
