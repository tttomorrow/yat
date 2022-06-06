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
--  @testpoint:vacuum命令，选项带括号，参数顺序不按语法要求，可以正常使用
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0076开始执行-----------------------------')

    def test_vacuum(self):
        # 创建列存表并插入数据
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
      CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER,WR_RETURNED_TIME_name varchar(200));
      insert into customer_info values (generate_series(1,2000),'a');''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd1)
        # 修改表数据
        sql_cmd2 = commonsh.execut_db_sql('''update customer_info set WR_RETURNED_TIME_name='c' where WR_RETURNED_DATE_SK >1000 and WR_RETURNED_DATE_SK<2000;
      select n_tup_ins,n_tup_upd,n_tup_del,n_live_tup,n_dead_tup,last_vacuum,last_data_changed from pg_stat_all_tables where relname='customer_info';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.UPDATE_SUCCESS_MSG, sql_cmd2)
        # 执行vacuum操作
        sql_cmd3 = commonsh.execut_db_sql('''vacuum (analyze,freeze,full)  customer_info;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.VACUUM_SUCCESS_MSG, sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd4 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0076执行结束--------------------------')
