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
--  @testpoint:VACUUM 仅回收空间，不更新统计信息，添加COMPACT参数
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0061开始执行-----------------------------')

    def test_vacuum(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
                                      CREATE TABLE customer_info(WR_RETURNED_DATE_SK serial,WR_RETURNED_TIME_SK INTEGER ,WR_ITEM_SK INTEGER NOT NULL,WR_REFUNDED_CUSTOMER_SK INTEGER);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 插入数据；删除一条数据
        sql_cmd2 = commonsh.execut_db_sql('''insert into customer_info values (101,2,5,8);
                                       insert into customer_info values (102,2,5,8);
                                       insert into customer_info values (103,2,5,8);
                                       delete from customer_info where WR_RETURNED_DATE_SK=102;''')

        logger.info(sql_cmd2)
        self.assertIn(constant.DELETE_SUCCESS_MSG, sql_cmd2)
        # vacuum full添加关键字COMPACT;vacuum freeze添加关键字COMPACT，合理报错;vacuum verbose添加关键字COMPACT，合理报错
        sql_cmd3 = commonsh.execut_db_sql(''' vacuum full COMPACT customer_info;
                                        vacuum freeze COMPACT customer_info;
                                        vacuum verbose COMPACT customer_info;
       ''')
        logger.info(sql_cmd3)
        self.assertIn(constant.VACUUM_SUCCESS_MSG, sql_cmd3)
        self.assertIn('ERROR:  COMPACT can only be used with VACUUM FULL', sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd4 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0061执行结束--------------------------')
