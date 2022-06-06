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
Case Type   : vacuum deltamerge
Case Name   : 列存表执行vacuum deltamerge
Description :
    1.建表并插入数据
    2.查询表体积
    3.执行vacuum deltamerge操作
    4.查询表大小
    5.删表
Expect      :
    1.建表成功且数据插入成功
    2.查询成功
    3.vacuum执行成功
    4.vacuum执行成功，表大小未变化
    5.表删除成功
History     :
"""
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0140开始执行-----------------------------')

    def test_vacuum(self):
        # 建表并插入数据
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
       CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER ,WR_RETURNED_TIME_name varchar(200))WITH (ORIENTATION = COLUMN);
       insert into customer_info values (generate_series(1,2320),'a');
       select pg_size_pretty(pg_relation_size('customer_info'));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd1)
        # 执行vacuum deltamerge操作，并查询表体积
        sql_cmd2 = commonsh.execut_db_sql('''vacuum deltamerge customer_info;
       select pg_size_pretty(pg_relation_size('customer_info'));''')
        logger.info(sql_cmd2)
        self.assertIn('DELTA MERGE',sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0140执行结束--------------------------')
