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
--  @testpoint:使用analyze收集普通表的单列统计信息,表名前加schema限定
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0094开始执行-----------------------------')

    def test_analyze(self):
        # 创建schema并创建表
        sql_cmd1 = commonsh.execut_db_sql('''drop schema if exists myschema;
create schema myschema;
drop table if exists myschema.customer_info;
CREATE TABLE myschema.customer_info(WR_RETURNED_DATE_SK INTEGER ,WR_RETURNED_TIME_name varchar(200) );
insert into myschema.customer_info values(generate_series(1,200),'a');''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_SCHEMA_SUCCESS_MSG, sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd1)
        # 使用ANALYZE语句
        sql_cmd2 = commonsh.execut_db_sql('''ANALYZE myschema.customer_info(WR_RETURNED_DATE_SK);
        ANALYZE verbose myschema.customer_info;
        select attname,null_frac,n_distinct,n_dndistinct from PG_STATS where tablename='customer_info';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.ANALYZE_SUCCESS_MSG, sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表和模式
        sql_cmd3 = commonsh.execut_db_sql('''drop table myschema.customer_info;
        drop schema myschema;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0094执行结束--------------------------')
