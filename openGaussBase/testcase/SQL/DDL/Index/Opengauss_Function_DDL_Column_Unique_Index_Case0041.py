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
Case Type   : DDL
Case Name   : 开启多个事务，session1中创建唯一索引，插入数据，session2中插入相同数据，先提交session1
Description :
    1.创建列存表
    2.开启两个会话，同时插入数据
    3.校验数据是否插入成功
    4.清理环境
Expect      :
    1.创建列存表成功
    2.开启两个会话，同时插入数据，其中一个会话插入失败
    3.校验数据，插入1000条数据成功
    4.清理环境成功
History     :
"""
import time
import unittest
from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DdlTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_DDL_Column_Unique_Index_Case0041开始')
        self.constant = Constant()
        self.commonsh1 = CommonSH('PrimaryDbUser')
        self.commonsh2 = CommonSH('PrimaryDbUser')
        self.tb_name = 't_column_tab_0041'
        self.index_name = 'i_column_index_0041'

    def test_unique_index(self):
        text1 = '-----step1.创建列存表; expect:列存表创建成功-----'
        self.log.info(text1)
        sql_cmd = self.commonsh1.execut_db_sql(
            f'drop table if exists {self.tb_name};'
            f'create table {self.tb_name}(id1 varchar,id2 int primary key) '
            f'with(orientation=column);')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd,
                      '执行失败:' + text1)

        text2 = '---step2.1session1开启事务插入数据，待session2开启后，' \
                '提交session1; expect:事务提交成功，数据成功插入---'
        self.log.info(text2)
        sql_01 = f"start transaction;" \
            f"create unique index {self.index_name} on {self.tb_name} " \
            f"using btree(id2);" \
            f"insert into {self.tb_name} values('column_' || " \
            f"generate_series(1,1000),generate_series(1,1000));" \
            f"select pg_sleep(10);" \
            f"commit;"

        thread_1 = ComThread(self.commonsh1.execut_db_sql, args=(sql_01, ''))
        thread_1.setDaemon(True)
        thread_1.start()
        time.sleep(1)

        text3 = '---step2.2 session2开启事务插入数据; expect:事务阻塞，' \
                'session1提交后，session2合理报错---'
        self.log.info(text3)
        sql_02 = f"select pg_sleep(2);" \
            f"start transaction;" \
            f"insert into {self.tb_name} values('column_' || " \
            f"generate_series(1,1000),generate_series(1,1000));"

        thread_2 = ComThread(self.commonsh2.execut_db_sql, args=(sql_02, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        thread_2.join(5)
        msg_result_2_1 = thread_2.get_result()
        self.log.info(msg_result_2_1)

        thread_1.join(20)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)

        thread_2.join(30)
        msg_result_2_2 = thread_2.get_result()
        self.log.info(msg_result_2_2)

        self.assertEqual(None, msg_result_2_1, '执行失败:' + text3)
        expect_msg1 = f'duplicate key value violates ' \
            f'unique constraint \"t_column_tab_0041_pkey\"'
        result = msg_result_1 + msg_result_2_2
        self.assertEqual(result.count(expect_msg1), 1, '执行失败:' + text3)
        self.assertEqual(result.count('START TRANSACTION'), 2,
                         '执行失败:' + text2 + text3)
        self.assertIn('CREATE INDEX', msg_result_1, '执行失败:' + text2)
        self.assertIn('INSERT 0 1000', msg_result_1, '执行失败:' + text2)
        self.assertIn('COMMIT', msg_result_1, '执行失败:' + text2)

        text4 = '---step3.校验数据是否插入成功; expect:只有session1插入了1000条数据---'
        self.log.info(text4)
        sql_cmd = self.commonsh1.execut_db_sql(
            f'select count(*) from {self.tb_name};')
        self.log.info(sql_cmd)
        self.assertIn('1000', sql_cmd)

    def tearDown(self):
        text5 = '--step4.清理环境; expect:清理数据成功--'
        self.log.info(text5)
        sql_cmd = self.commonsh1.execut_db_sql(f'drop table {self.tb_name};')
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_DDL_Column_Unique_Index_Case0041结束')