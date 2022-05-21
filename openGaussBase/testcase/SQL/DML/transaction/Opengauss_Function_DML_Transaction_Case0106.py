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
Case Name   : 设置session会话的事务隔离级别为REPEATABLE READ，对表进行插入操作后不提交，
              新起session设置事务隔离级别为REPEATABLE READ，插入数据是否可以查询到
Description :
    1.创建测试表
    CREATE TABLE TESTZL (
        SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
    2.设置session事务隔离级别为REPEATABLE READ
    SET SESSION CHARACTERISTICS AS TRANSACTION
    ISOLATION LEVEL REPEATABLE READ ;
    3.查看设置的事务隔离级别是否生效
    SHOW TRANSACTION_ISOLATION;
    4.对数据库表执行插入操作
    INSERT INTO TESTZL VALUES(001,'SK1','TT',3332);
    5.新起事务，设置session事务隔离级别为REPEATABLE READ
    SET SESSION CHARACTERISTICS AS TRANSACTION
    ISOLATION LEVEL REPEATABLE READ ;
    6.查看设置的事务隔离级别是否生效
    SHOW TRANSACTION_ISOLATION;
    7.查看插入数据
    SELECT * FROM TESTZL;
    8.清理环境
    DROP TABLE IF EXISTS TESTZL;
Expect      :
    1.创建测试表成功
    2.设置session事务隔离级别为REPEATABLE READ成功
    3.设置的事务隔离级别已生效
    4.对数据库表执行插入操作成功
    5.新起事务，设置session事务隔离级别为REPEATABLE READ成功
    6.设置的事务隔离级别已生效
    7.查看插入数据成功，数据同步
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


class TransactionFile(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_DML_Transaction_Case0106开始执行----')
        self.constant = Constant()
        self.t_name = 't_dml_transaction_case0106'

    def test_transaction_file(self):
        step1_txt = '----step1：创建测试表 expect:创建成功----'
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
        step4_txt = '----step4：对数据库表执行插入操作 expect:插入成功----'
        self.log.info(step4_txt)
        sql_cmd4 = f"INSERT INTO {self.t_name} VALUES(001,'SK1','TT',3332);"
        step5_txt = '----step5：新起事务，设置session事务隔离级别为REPEATABLE READ' \
                    ' expect:新起事务成功----'
        self.log.info(step5_txt)
        sql_cmd5 = f'SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION ' \
            f'LEVEL REPEATABLE READ ;'
        step6_txt = '----step6：查看设置的事务隔离级别是否生效 expect:已生效----'
        self.log.info(step6_txt)
        sql_cmd6 = 'SHOW TRANSACTION_ISOLATION;'
        step7_txt = '----step7：查看插入数据 expect:数据同步----'
        self.log.info(step7_txt)
        sql_cmd7 = f"SELECT * FROM {self.t_name} WHERE SK = 1;"

        threads = []
        self.log.info('----事务1操作: step1-step2-step3-step6----')
        tras_sql1 = f'{sql_cmd1}' \
            f'{sql_cmd2}' \
            f'{sql_cmd3}' \
            f'{sql_cmd4}'
        session1 = ComThread(Primary_SH.execut_db_sql, args=(tras_sql1,))
        threads.append(session1)

        self.log.info('----事务2操作: step4-step5-step7----')
        tras_sql2 = f'SELECT PG_SLEEP(5);' \
            f'{sql_cmd5}' \
            f'{sql_cmd6}' \
            f'{sql_cmd7}'
        session2 = ComThread(Primary_SH.execut_db_sql, args=(tras_sql2,))
        threads.append(session2)

        self.log.info('----启动线程----')
        thread_results = []
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join(15)
            thread_results.append(t.get_result())
            self.log.info(t.get_result())
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, thread_results[0],
                      '执行失败:' + step1_txt)
        self.assertIn(self.constant.SET_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step2_txt)
        self.assertIn(self.constant.REPEATABLE_READ_MSG, thread_results[0],
                      '执行失败:' + step3_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, thread_results[0],
                      '执行失败:' + step4_txt)
        self.assertIn(self.constant.SET_SUCCESS_MSG, thread_results[1],
                      '执行失败:' + step5_txt)
        self.assertIn(self.constant.REPEATABLE_READ_MSG, thread_results[1],
                      '执行失败:' + step6_txt)
        ses2_res7 = thread_results[1].splitlines()[-1].strip()
        self.assertIn('1 row', ses2_res7, '执行失败:' + step7_txt)

    def tearDown(self):
        self.log.info('----清理环境----')
        text = '----删除表 expect:成功----'
        self.log.info(text)
        drop_sql = f'DROP TABLE IF EXISTS {self.t_name};'
        drop_msg = Primary_SH.execut_db_sql(drop_sql)
        self.log.info(drop_msg)
        self.log.info(
            '----Opengauss_Function_DML_Transaction_Case0106执行完成----')

        self.log.info('----断言tearDown执行成功----')
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text)
