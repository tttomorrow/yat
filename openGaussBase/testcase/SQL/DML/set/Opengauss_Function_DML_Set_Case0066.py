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
--  @testpoint:vvacuum清理具体字段名称，不加analyze，合理报错
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0066开始执行-----------------------------')

    def test_vacuum(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
                                      CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER,WR_RETURNED_TIME_name varchar(200));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 查看表的字节大小（建表后，未做任何操作字节为0）；插入数据，查看表的字节大小，有变化
        # 分别插入数据，删除创建，查看系统表信息，行数更新为4001
        sql_cmd2 = commonsh.execut_db_sql('''select pg_size_pretty(pg_relation_size('customer_info'));
        insert into customer_info values (generate_series(1,2000),'a');
        insert into customer_info values (generate_series(2001,5000),'b');
        select relpages,reltuples from pg_class where relname='customer_info';
        delete from customer_info where WR_RETURNED_DATE_SK>4000 and WR_RETURNED_DATE_SK<5000;
        vacuum full customer_info(WR_RETURNED_DATE_SK);
        select relpages,reltuples from pg_class where relname='customer_info';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.DELETE_SUCCESS_MSG, sql_cmd2)
        self.assertIn('ERROR:  syntax error', sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd4 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0066执行结束--------------------------')
