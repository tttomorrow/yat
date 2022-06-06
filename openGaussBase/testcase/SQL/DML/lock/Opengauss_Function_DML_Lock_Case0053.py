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
Case Name   : 指定only对数据库表枷锁后更新该表的子表
Description :
    1.创建测试表并增加继承关系
      1.1.创建父表
      1.2.创建子表
      1.3 给两张表增加继承关系
    2.开启session1，开启事务，指定only对父表加锁，不做提交
    3.不关闭session1，开启session2，对子表进行更新
    4，清理环境
Expect      :
    1.创建测试表并增加继承关系成功
      1.1.创建父表成功
      1.2.创建子表成功
      1.3 给两张表增加继承关系成功
    2.开启session1，开启事务，指定only对父表加锁，不做提交，加锁成功
    3.对子表进行更新成功，事务未阻塞
    4，清理环境成功
History     :
"""

import unittest
from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class LockTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_DML_Lock_Case0052 开始执行')
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')
        self.tb_name1 = 't_f_lock_0051'
        self.tb_name2 = 't_s_lock_0051'

    def test_dml_lock(self):
        text = '-----step1: 创建测试表并增加继承关系; expect: 创建表并增加继承关系成功-----'
        self.log.info(text)
        text = '-----step1.1: 创建父表; expect: 创建父表功-----'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"drop table if exists {self.tb_name1};"
            f"CREATE TABLE {self.tb_name1} (name varchar,population "
            f"integer,altitude integer);")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = '-----step1.2: 创建子表; expect: 创建子表功-----'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"drop table if exists {self.tb_name2};"
            f"create table {self.tb_name2} (name varchar,population integer,"
            f"altitude integer,state varchar) ;")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = '-----step1.3: 给两张表增加继承关系; expect: 给两张表增加继承关系成功-----'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"alter table {self.tb_name2} INHERIT {self.tb_name1};")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.ALTER_TABLE_MSG, sql_cmd,
                      '执行失败:' + text)

        text2 = '-step2: 开启session1，开启事务，指定only对父表加锁，不做提交;' \
                ' expect: 加锁成功-'
        self.log.info(text2)
        sql = f"start transaction;" \
            f"lock table only {self.tb_name1} in access exclusive mode;" \
            f"select pg_sleep(15);" \
            f"select timenow();"
        thread_1 = ComThread(self.commonsh.execut_db_sql, args=(sql, ''))
        thread_1.setDaemon(True)
        thread_1.start()

        text3 = 'step3: 不关闭session1，开启session2，对子表进行更新;' \
                ' expect: 对子表进行更新成功，事务未阻塞'
        self.log.info(text3)
        sql = f"select pg_sleep(3);" \
            f"start transaction;" \
            f"insert into {self.tb_name2} values ('aaa',001,315,'nomal');"
        thread_2 = ComThread(self.commonsh.execut_db_sql, args=(sql, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        thread_1.join(20)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)

        thread_2.join(5)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)

        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG,
                      msg_result_1, '执行失败:' + text2)
        self.assertIn(self.constant.LOCK_TABLE_MSG,
                      msg_result_1, '执行失败:' + text2)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG,
                      msg_result_2, '执行失败:' + text3)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG,
                      msg_result_2, '执行失败:' + text3)

    def tearDown(self):
        text = '--step4: 清理环境; expect: 清理成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"drop table if exists {self.tb_name1} cascade;")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.log.info('Opengauss_Function_DML_Lock_Case0052 执行结束')
