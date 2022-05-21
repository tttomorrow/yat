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
Case Name   : 在隔离级别为READ COMMITTED的session事务中开启local事务是否成功
Description :
    1.创建测试表
    CREATE TABLE TESTZL (
        SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
    2.设置session事务隔离级别为REPEATABLE READ
    SET SESSION CHARACTERISTICS AS TRANSACTION
    ISOLATION LEVEL REPEATABLE READ ;
    3.查看设置的事务隔离级别是否生效
    SHOW TRANSACTION_ISOLATION;
    4.新起事务，并设置session事务隔离级别READ COMMITTED
    SET SESSION CHARACTERISTICS AS TRANSACTION
    ISOLATION LEVEL READ COMMITTED ;
    5.在第一个事务中进行插入操作
    INSERT INTO TESTZL VALUES(001,'SK2','TT',3332);
    6.第二个事务中开启事务
    START TRANSACTION;
    7.设置第二个事务为local事务，隔离级别为REPEATABLE READ
    SET LOCAL TRANSACTION ISOLATION LEVEL REPEATABLE READ ;
    8.在第二个事务中进行数据查询
    SELECT * FROM TESTZL;
    9.在第一个事务中进行插入操作
    INSERT INTO TESTZL VALUES(002,'SK2','TT',3332);
    10.在第二个事务中进行数据查询
    SELECT * FROM TESTZL;
    11.清理环境
    DROP TABLE IF EXISTS TESTZL;
Expect      :
    1.创建测试表成功
    2.设置session事务隔离级别为REPEATABLE READ成功
    3.设置的事务隔离级别已生效
    4.新起事务，并设置session事务隔离级别READ COMMITTED成功
    5.在第一个事务中进行插入操作成功
    6.直接开启事务成功
    7.设置第二个事务为local事务，隔离级别为REPEATABLE READ成功
    8.在第二个事务中进行数据查询成功
    9.在第一个事务中进行插入操作成功
    10.在第二个事务中进行数据查询失败，查询不到最新更新的数据
    11.清理环境成功
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


class TransactionFile(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_DML_Transaction_Case0108开始执行----')
        self.constant = Constant()
        self.t_name = 't_dml_transaction_case0108'

    def test_transaction_file(self):
        step1_txt = '----step1：创建测试表 expect:----'
        self.log.info(step1_txt)
        sql_cmd1 = f"DROP TABLE IF EXISTS {self.t_name};" \
            f"CREATE TABLE {self.t_name} (" \
            f"SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);"
        step2_txt = '----step2：设置session事务隔离级别为REPEATABLE READ ' \
                    'expect:设置成功----'
        self.log.info(step2_txt)
        sql_cmd2 = "SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION " \
                   "LEVEL REPEATABLE READ ;"
        step3_txt = '----step3：查看设置的事务隔离级别是否生效 expect:已生效----'
        self.log.info(step3_txt)
        sql_cmd3 = "SHOW TRANSACTION_ISOLATION;"
        step4_txt = '----step4：新起事务，并设置session事务隔离级别' \
                    'READ COMMITTED expect:设置成功----'
        self.log.info(step4_txt)
        sql_cmd4 = 'SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION ' \
                   'LEVEL READ COMMITTED ;'
        step5_txt = '----step5：在第一个事务中进行插入操作 expect:插入成功----'
        self.log.info(step5_txt)
        sql_cmd5 = f"INSERT INTO {self.t_name} VALUES(001,'SK2','TT',3332);"
        step6_txt = '----step6：第二个事务中开启事务 expect:开启成功----'
        self.log.info(step6_txt)
        sql_cmd6 = 'START TRANSACTION;'
        step7_txt = '----step7：设置第二个事务为local事务，隔离级别为' \
                    'REPEATABLE READ expect:设置成功----'
        self.log.info(step7_txt)
        sql_cmd7 = 'SET LOCAL TRANSACTION ISOLATION LEVEL REPEATABLE READ ;'
        step8_txt = '----step8：在第二个事务中进行数据查询 expect:查询成功----'
        self.log.info(step8_txt)
        sql_cmd8 = f"SELECT * FROM {self.t_name} WHERE SK = 1;"
        step9_txt = '----step9：在第一个事务中进行插入操作 expect:插入成功----'
        self.log.info(step9_txt)
        sql_cmd9 = f"INSERT INTO {self.t_name} VALUES(002,'SK2','TT',3332);"
        step10_txt = '----step10：在第二个事务中进行数据查询 expect:查询不到最新更新的数据----'
        self.log.info(step10_txt)
        sql_cmd10 = f"SELECT * FROM {self.t_name} WHERE SK = 2;"

        threads = []
        self.log.info('----线程1操作事务1:step1-step2-step3-step5-step9----')
        tras_sql1 = f'{sql_cmd1}' \
            f'{sql_cmd2}' \
            f'{sql_cmd3}' \
            f'SELECT PG_SLEEP(15);' \
            f'{sql_cmd5}' \
            f'SELECT PG_SLEEP(18);' \
            f'{sql_cmd9}'
        session1 = ComThread(Primary_SH.execut_db_sql, args=(tras_sql1,))
        threads.append(session1)

        self.log.info('----线程2操作事务2:step4-step6-step7-step8-step10----')
        tras_sql2 = f'SELECT PG_SLEEP(12);' \
            f'{sql_cmd4}' \
            f'SELECT PG_SLEEP(15);' \
            f'{sql_cmd6}' \
            f'{sql_cmd7}' \
            f'{sql_cmd8}' \
            f'SELECT PG_SLEEP(18);' \
            f'{sql_cmd10}'
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
        self.assertIn(self.constant.SET_SUCCESS_MSG,
                      thread_results[0], '执行失败:' + step2_txt)
        self.assertIn(self.constant.REPEATABLE_READ_MSG, thread_results[0],
                      '执行失败:' + step3_txt)
        self.assertIn(self.constant.SET_SUCCESS_MSG, thread_results[1],
                      '执行失败:' + step4_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step5_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG,
                      thread_results[1], '执行失败:' + step6_txt)
        self.assertIn(self.constant.SET_SUCCESS_MSG, thread_results[1],
                      '执行失败:' + step7_txt)
        ses2_res8 = thread_results[1].splitlines()[-10].strip()
        self.assertIn('1 row', ses2_res8, '执行失败:' + step8_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step9_txt)
        ses2_res10 = thread_results[1].splitlines()[-1].strip()
        self.assertIn('0 row', ses2_res10, '执行失败:' + step10_txt)

    def tearDown(self):
        self.log.info('----清理环境----')
        text = '----删除表 expect:成功----'
        self.log.info(text)
        drop_sql = f'DROP TABLE IF EXISTS {self.t_name};'
        drop_msg = Primary_SH.execut_db_sql(drop_sql)
        self.log.info(drop_msg)
        self.log.info(
            '----Opengauss_Function_DML_Transaction_Case0108执行完成----')

        self.log.info('----断言tearDown执行成功----')
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text)
