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
Case Type   : 事务控制
Case Name   : 两个事务的隔离级别设为READ COMMITTED，一个事务提交后在新的事务中
              是否可以查看到已提交事务数据，执行后查看备机数据
Description :
    1.创建测试表
    DROP TABLE IF EXISTS TEST_TRAN;
    CREATE TABLE TEST_TRAN (
        SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
    2.开启事务并指定事务隔离级别为READ COMMITTED
    START TRANSACTION ISOLATION LEVEL READ COMMITTED READ WRITE;
    3.在事务中对数据库表插入一条数据
    INSERT INTO TEST_TRAN VALUES (001,'SK1','TT',3332);
    4.开启新的事务，并指定指定事务隔离级别为READ COMMITTED
    START TRANSACTION ISOLATION LEVEL READ COMMITTED READ WRITE;
    5.提交第一个事务
    COMMIT;
    6.在第二个事务中查询第一个事务数据
    SELECT * FROM TEST_TRAN WHERE SK = 1;
    7.查看备机数据是否同步
    SELECT * FROM TEST_TRAN;
    8.清理环境
    DROP TABLE IF EXISTS TEST_TRAN;
Expect      :
    1.创建测试表成功
    2.开启事务并指定事务隔离级别为READ COMMITTED成功
    3.在事务中对数据库表插入一条数据成功
    4.开启新的事务，并指定指定事务隔离级别为READ COMMITTED成功
    5.提交第一个事务成功
    6.在第二个事务中查询第一个事务数据成功
    7.备机数据同步成功
    8.清理环境成功
History     :
"""

import time
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.ComThread import ComThread
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(), '单机环境不执行')
class TransactionFile(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_DML_Transaction_Case0007开始执行----')
        self.Standby_SH = CommonSH('Standby1DbUser')
        self.constant = Constant()
        self.t_name = 't_dml_transaction_case0007'

    def test_transaction_file(self):
        step1_txt = '----step1：创建测试表 expect:创建成功----'
        self.log.info(step1_txt)
        sql_cmd1 = f"DROP TABLE IF EXISTS {self.t_name};" \
            f"CREATE TABLE {self.t_name} (" \
            f"SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);"
        step2_txt = '----step2：开启事务并指定事务隔离级别为READ COMMITTED ' \
                    'expect:开启设置事务成功----'
        self.log.info(step2_txt)
        sql_cmd2 = "START TRANSACTION ISOLATION LEVEL" \
                   " READ COMMITTED READ WRITE;"
        step3_txt = '----step3：在事务中对数据库表插入一条数据 expect:插入成功----'
        self.log.info(step3_txt)
        sql_cmd3 = f"INSERT INTO {self.t_name} VALUES (001,'SK1','TT',3332);"
        step4_txt = '----step4：开启新的事务，并指定指定事务隔离级别为' \
                    'READ COMMITTED expect:开启设置事务成功----'
        self.log.info(step4_txt)
        sql_cmd4 = 'START TRANSACTION ISOLATION LEVEL ' \
                   'READ COMMITTED READ WRITE;'
        step5_txt = '----step5：提交第一个事务 expect:提交成功----'
        self.log.info(step5_txt)
        sql_cmd5 = 'COMMIT;'
        step6_txt = '----step6：在第二个事务中查询第一个事务数据 expect:查询成功----'
        self.log.info(step6_txt)
        sql_cmd6 = f"SELECT * FROM {self.t_name} WHERE SK = 1;"

        threads = []
        self.log.info('----事务1操作: step1-step2-step3-step5----')
        tras_sql1 = f'{sql_cmd1}' \
            f'{sql_cmd2}' \
            f'{sql_cmd3}' \
            f'SELECT PG_SLEEP(15);' \
            f'{sql_cmd5}'
        session1 = ComThread(Primary_SH.execut_db_sql, args=(tras_sql1,))
        threads.append(session1)

        self.log.info('----事务2操作: step4-step6----')
        tras_sql2 = f'SELECT PG_SLEEP(12);' \
            f'{sql_cmd4}' \
            f'SELECT PG_SLEEP(15);' \
            f'{sql_cmd6}'
        session2 = ComThread(Primary_SH.execut_db_sql, args=(tras_sql2,))
        threads.append(session2)

        self.log.info('----启动线程----')
        thread_results = []
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join(60)
            thread_results.append(t.get_result())
            self.log.info(t.get_result())
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG,
                      thread_results[0], '执行失败:' + step2_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step3_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG,
                      thread_results[1], '执行失败:' + step4_txt)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step5_txt)
        ses2_res6 = thread_results[1].splitlines()[-1].strip()
        self.assertIn('1 row', ses2_res6, '执行失败:' + step6_txt)

        step7_txt = '----step7：查看备机数据是否同步 expect:同步成功----'
        self.log.info(step7_txt)
        sql_cmd7 = f'SELECT * FROM {self.t_name};'
        msg_primary = Primary_SH.execut_db_sql(sql_cmd7)
        self.log.info(msg_primary)
        msg_standby = self.Standby_SH.execut_db_sql(sql_cmd7)
        self.log.info(msg_standby)
        self.assertEqual(msg_primary, msg_standby, '执行失败:' + step7_txt)

    def tearDown(self):
        self.log.info('----清理环境----')
        text = '----删除表 expect:成功----'
        self.log.info(text)
        drop_sql = f'DROP TABLE IF EXISTS {self.t_name};'
        drop_msg = Primary_SH.execut_db_sql(drop_sql)
        self.log.info(drop_msg)
        self.log.info(
            '----Opengauss_Function_DML_Transaction_Case0007执行完成----')

        self.log.info('----断言tearDown执行成功----')
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text)
