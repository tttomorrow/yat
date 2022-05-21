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
'''
--  @testpoint:explain analyze分析EXECUTE语句
'''
import sys
import unittest
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0134开始执行-----------------------------')

    def test_explain(self):
        # 建表并插入数据
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists reason;
       CREATE TABLE reason (CD_DEMO_SK INTEGER NOT NULL,CD_GENDER character(16),CD_MARITAL_STATUS character(100));
       INSERT INTO reason VALUES(51, 'AAAAAAAADDAAAAAA', 'reason 51');''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd1)
        # 创建表reason_t1;为一个INSERT语句创建一个预备语句并执行，reason_t1表插入一条数据
        #  # 事务中，explain analyze执行预备语句（reason_t1表插入一条数据）；回滚（reason_t1表恢复为两条数据，执行预备语句的数据撤销）
        sql_cmd2 = commonsh.execut_db_sql('''drop table if exists reason_t1;
       CREATE TABLE reason_t1 AS TABLE reason;
       PREPARE insert_reason(integer,character(16),character(100)) AS INSERT INTO reason_t1 VALUES(\$1,\$2,\$3);
       EXECUTE insert_reason(52, 'AAAAAAAADDAAAAAA', 'reason 52');
       select * from reason_t1;
       start transaction;
        explain analyze verbose EXECUTE insert_reason(53, 'AAAAAAAADDAAAAAA', 'reason 53');
        select * from reason_t1;
        rollback;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.PREPARE_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.EXPLAIN_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.ROLLBACK_MSG, sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''drop table reason;
       drop table reason_t1;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0134执行结束--------------------------')
