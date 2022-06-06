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
Case Name   : 数据表加exclusive锁后是否可以进行更新操作
Description :
    1.创建测试表并插入数据
    2.开启事务，对表加exclusive锁,不做提交
    3.开启新的事务，对表进行update操作，不做提交
    4.清理环境
Expect      :
    1.创建测试表并插入数据成功
    2.开启事务，对表加exclusive锁，不做提交操作成功
    3.开启新的事务，对表进行update操作，不做提交失败，事务阻塞
    4.清理环境成功
History     :
"""
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DmlTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_DML_Lock_Case0007开始')
        self.constant = Constant()
        self.commonsh1 = CommonSH('PrimaryDbUser')
        self.commonsh2 = CommonSH('PrimaryDbUser')
        self.tb_name = 't_lock_0007'

    def test_dml_lock(self):
        text1 = '-----step1: 创建测试表; expect: 创建表并插入数据成功-----'
        self.log.info(text1)
        sql_cmd = self.commonsh1.execut_db_sql(
            f"drop table if exists {self.tb_name};"
            f"create table {self.tb_name}(sk integer,id char(16),"
            f"name varchar(20),sq_ft integer);"
            f"insert into {self.tb_name} values (001,'sk1','tt',3332);")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd,
                      '执行失败:' + text1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text1)

        text2 = '-----step2: 开启事务，对表加exclusive锁，' \
                '然后进行select操作，不做提交，在session2执行update后，' \
                '再次查看表数据; expect: session1 未commit前表数据更新失败-----'
        self.log.info(text2)
        sql = f"start transaction;" \
              f"lock table {self.tb_name} in exclusive mode;" \
              f"select * from {self.tb_name};" \
              f"select pg_sleep(5);" \
              f"select * from {self.tb_name};"
        thread_1 = ComThread(self.commonsh2.execut_db_sql, args=(sql, ''))
        thread_1.setDaemon(True)
        thread_1.start()

        text3 = '-----step3: 开启新的事务，对表进行update操作，' \
                '不做提交; expect: session1未提交之前，事务阻塞-----'
        self.log.info(text3)
        sql = f"select pg_sleep(3);" \
              f"start transaction;" \
              f"select timenow();" \
              f"update {self.tb_name} set id ='sk5' where sk = 1;"
        thread_2 = ComThread(self.commonsh1.execut_db_sql, args=(sql, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        thread_1.join(30)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)

        thread_2.join(1)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)

        assert_eq_1 = msg_result_1.count('START TRANSACTION') is 1
        assert_eq_2 = msg_result_1.count(
            '  1 | sk1              | tt   |  3332') is 2
        self.assertTrue(assert_eq_1 and assert_eq_2, '执行失败:' + text2)
        assert_eq_3 = msg_result_2.count('START TRANSACTION') is 1
        self.assertTrue(assert_eq_3, '执行失败:' + text3)

    def tearDown(self):
        text = '--step4: 清理环境; expect: 清理成功--'
        self.log.info(text)
        sql_cmd = self.commonsh1.execut_db_sql(
            f"drop table if exists {self.tb_name};")
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_DML_Lock_Case0007结束')
