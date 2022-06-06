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
--  @testpoint:analyze检测表的数据文件
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0102开始执行-----------------------------')

    def test_analyze(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
       CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER ,WR_RETURNED_TIME_name varchar(200) );''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 执行analyze语句
        sql_cmd2 = commonsh.execut_db_sql('''ANALYZE VERIFY fast customer_info CASCADE;
        ANALYZE VERIFY COMPLETE customer_info CASCADE;
        select relname,last_autovacuum,last_analyze from pg_stat_user_tables where relname='customer_info';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.ANALYZE_SUCCESS_MSG, sql_cmd2)
        # 创建索引;对索引表执行analyze
        sql_cmd3 = commonsh.execut_db_sql('''drop index if exists WR_RETURNED_DATE_SK_uni cascade;
       create unique index WR_RETURNED_DATE_SK_uni on customer_info(WR_RETURNED_DATE_SK);
       ANALYZE VERIFY fast WR_RETURNED_DATE_SK_uni;
       ANALYZE VERIFY COMPLETE WR_RETURNED_DATE_SK_uni;''')
        self.assertIn(constant.CREATE_INDEX_SUCCESS_MSG, sql_cmd3)
        self.assertIn(constant.ANALYZE_SUCCESS_MSG, sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd3 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0102执行结束--------------------------')
