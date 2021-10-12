"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
--  @date:2020/08/19
--  @testpoint:创建联合唯一约束，并定义其中一列是序列型
'''
import sys
import unittest
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Upsert_Case0078开始执行-----------------------------')
    def test_sysadmin_user_permission(self):
        # 建表并创建联合唯一索引
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists t5;
                                      CREATE TABLE t5 (col1 INT,col2 INT DEFAULT 1,col3 BIGSERIAL,col5 INTEGER(10, 5) DEFAULT RANDOM() + 1);
                                      CREATE UNIQUE INDEX u_t5_index1 ON t5(col1, col3);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 插入三条数据，联合唯一约束均不重复，插入三条数据(1,1,1,RANDOM() + 1);(1,1,2,RANDOM() + 1);(1,1,3,RANDOM() + 1)
        # 插入一条数据，联合唯一约束均不重复，col列不给值，其余列使用默认值,新增一条数据(,1,4,RANDOM() + 1)
        # 根据 col3降序排序
        # 插入三条数据，联合唯一约束均重复，故更新三条数据，更新后为(1,10,1,1);(1,20,2,1);(1,30,3,1)
        # 联合主键均不重复，插入两条数据(2,1,5,RANDOM() + 1);(2,1,6,RANDOM() + 1)

        sql_cmd2 = commonsh.execut_db_sql('''INSERT INTO t5 VALUES (1), (1), (1) ON DUPLICATE KEY UPDATE col2 = col3;
                                      INSERT INTO t5 DEFAULT VALUES ON DUPLICATE KEY UPDATE col2 = col3;
                                      SELECT * FROM t5 ORDER BY col3 desc;
                                      INSERT INTO t5 (col1, col3) VALUES (1, 1), (1, 2), (1, 3) ON DUPLICATE KEY UPDATE col5 = col2, col2 = col3 * 10;
                                      INSERT INTO t5 (col1, col3) VALUES (2, 5), (2, 6);
                                      INSERT INTO t5 (col1) VALUES (2), (2), (2) ON DUPLICATE KEY UPDATE col2 = col3;
                                      INSERT INTO t5 VALUES (2), (2);''')
        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
        # 根据col3列排序
        sql_cmd3 = commonsh.execut_db_sql('''SELECT col1, col2, col3 FROM t5 ORDER BY col3;''')
        logger.info(sql_cmd3)
        self.assertIn('col3', sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd4 = commonsh.execut_db_sql('''drop table t5;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DML_Upsert_Case0078执行结束--------------------------')





