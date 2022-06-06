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
--  @testpoint:创建联合主键约束，并定义其中一列是序列类型
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

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Upsert_Case0077开始执行-----------------------------')
    def test_sysadmin_user_permission(self):
        # 创建schema并设置当前schema
        sql_cmd1 = commonsh.execut_db_sql('''DROP SCHEMA if exists test_insert_update_010 CASCADE;
                                      CREATE SCHEMA test_insert_update_010;
                                      SET CURRENT_SCHEMA TO test_insert_update_010;
                                      select current_schema;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_SCHEMA_SUCCESS_MSG, sql_cmd1)
        # 建表
        sql_cmd2 = commonsh.execut_db_sql('''drop table if exists t4;
                                      CREATE TABLE t4 (col1 INT,col2 INT DEFAULT 0,col3 INT DEFAULT 1,col4 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,col5 BIGSERIAL,
                                      PRIMARY KEY (col2, col3, col5)) ;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_TABLE_SUCCESS, sql_cmd2)
        # 使用insert..update，联合主键col2, col3, col5均不重复，插入一条数据(1,0,1,CURRENT_TIMESTAMP,1)
        # 使用insert..update，联合主键col2, col3, col5均不重复，插入一条数据(1,0,1,CURRENT_TIMESTAMP,2)
        # 使用insert..update，联合主键不重复，插入一条数据(2,2,1,CURRENT_TIMESTAMP,3)
        # 使用insert..update，联合主键不重复，插入一条数据(100, 100, 100, CURRENT_TIMESTAMP, 100)
        sql_cmd3 = commonsh.execut_db_sql('''INSERT INTO t4 VALUES (1) ON DUPLICATE KEY UPDATE col1 = 10;
                                      INSERT INTO t4 VALUES (1) ON DUPLICATE KEY UPDATE col1 = 10;
                                      INSERT INTO t4 VALUES (2,2) ON DUPLICATE KEY UPDATE col1 = 200;
                                      INSERT INTO t4 VALUES (100, 100, 100, CURRENT_TIMESTAMP, 100) ON DUPLICATE KEY UPDATE col1 = 1000;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd3)
        # 根据col5列降序排序
        sql_cmd4 = commonsh.execut_db_sql('''SELECT col1, col2, col3, col5 FROM t4 ORDER BY col5 desc;''')
        logger.info(sql_cmd4)
        # 联合主键不重复，新增一条数据2, 2, 2, CURRENT_TIMESTAMP, 3)
        # 联合主键重复，更新col1列，数据(100, 100, 100, CURRENT_TIMESTAMP, 100)更改为(1000, 100, 100, CURRENT_TIMESTAMP, 100)
        sql_cmd5 = commonsh.execut_db_sql('''INSERT INTO t4 VALUES (2, 2, 2, CURRENT_TIMESTAMP, 3) ON DUPLICATE KEY UPDATE col1 = 200;
                                      INSERT INTO t4 VALUES (100, 100, 100, CURRENT_TIMESTAMP, 100) ON DUPLICATE KEY UPDATE col1 = 1000;''')
        logger.info(sql_cmd5)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd5)
        # 根据col5列降序排序
        sql_cmd6 = commonsh.execut_db_sql('''SELECT col1, col2, col3, col5 FROM t4 ORDER BY col5;''')
        logger.info(sql_cmd6)
        self.assertIn('col5', sql_cmd6)
       # 恢复schema为public
        sql_cmd7 = commonsh.execut_db_sql('''SET CURRENT_SCHEMA TO public;''')
        logger.info(sql_cmd7)
        self.assertIn('SET', sql_cmd7)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd8 = commonsh.execut_db_sql('''drop table t4;''')
        logger.info(sql_cmd8)
        logger.info('------------------------Opengauss_Function_DML_Upsert_Case0077执行结束--------------------------')





