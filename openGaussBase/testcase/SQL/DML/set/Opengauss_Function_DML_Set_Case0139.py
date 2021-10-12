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
"""
Case Type   : vacuum...delete
Case Name   : 对表执行vacuum full操作，回收delete操作标记过的存储空间
Description :
    1.建表并插入数据
    2.查询表体积并执行删除操作
    3.查询表记录数并查询表体积
    4.执行vacuum full操作并查询表大小
    5.删表
Expect      :
    1.建表成功且数据插入成功
    2.查询成功且删除成功
    3.记录数为0，体积未发生变化
    4.vacuum执行成功，表大小为0
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0139开始执行-----------------------------')

    def test_vacuum(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
       CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER ,WR_RETURNED_TIME_name varchar(200) );
       insert into customer_info values (generate_series(1,134528),'a');''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''select pg_size_pretty(pg_relation_size('customer_info'));
       delete from customer_info;
       select count(1) from customer_info;
       select pg_size_pretty(pg_relation_size('customer_info'));''')
        logger.info(sql_cmd2)
        self.assertIn(constant.DELETE_SUCCESS_MSG, sql_cmd2)
        self.assertIn('0', sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql('''vacuum full customer_info;
       select pg_size_pretty(pg_relation_size('customer_info'));''')
        logger.info(sql_cmd3)
        self.assertIn(constant.VACUUM_SUCCESS_MSG,sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0139执行结束--------------------------')
