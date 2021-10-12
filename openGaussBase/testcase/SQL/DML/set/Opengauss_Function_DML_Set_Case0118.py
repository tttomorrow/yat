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
Case Type   : analyze
Case Name   : 使用reindex重建索引，重建非当前连接数据库合理报错
Description :
              1、建表并创建索引
              2、重建索引,索引名不存在
              3、重建表和数据库（非当前数据库）
              4、清理环境
Expect      :
              1、建表并创建索引成功
              2、合理报错
              3、重建非当前连接数据库，ERROR:  can only reindex the currently
               open database
              4、清理环境完成
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

COMMONSH = CommonSH('PrimaryDbUser')
constant = Constant()


class SYS_Operation(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-------Opengauss_Function_DML_Set_Case0118开始执行-----')
        self.res = 'ERROR:  can only reindex the currently open database'

    def test_index(self):
        self.log.info('步骤1:建表并创建索引')
        sql_cmd1 = COMMONSH.execut_db_sql('''drop table if exists 
            customer_info;
            create table customer_info(wr_returned_date_sk integer ,
            wr_returned_time_name varchar(200));
            drop index if exists wr_returned_date_sk_index;
            create index wr_returned_date_sk_index on customer_info
            (wr_returned_date_sk);''')
        self.log.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.CREATE_INDEX_SUCCESS, sql_cmd1)
        self.log.info('步骤2:重建索引,索引名不存在，合理报错')
        sql_cmd2 = COMMONSH.execut_db_sql('''reindex index 
            wr_returned_date_sk_index;
            reindex index wr_returned_date_sk_index1;''')
        self.log.info(sql_cmd2)
        self.assertIn(constant.REINDEX_SUCCESS_MSG, sql_cmd2)
        self.assertIn(
            'ERROR:  relation "wr_returned_date_sk_index1" does not exist',
            sql_cmd2)
        self.log.info('步骤3:创建索引')
        sql_cmd3 = COMMONSH.execut_db_sql('''drop index if exists 
            wr_returned_time_name_index;
            create index wr_returned_time_name_index on customer_info
            (wr_returned_time_name);
            reindex table customer_info;
            reindex DATABASE postgres;''')
        self.log.info(sql_cmd3)
        self.assertIn(constant.CREATE_INDEX_SUCCESS, sql_cmd3)
        self.assertIn(constant.REINDEX_SUCCESS_MSG, sql_cmd3)
        self.assertIn(self.res, sql_cmd3)
        sql_cmd4 = COMMONSH.execut_db_sql('''drop database if exists test1;
            create database test1;
            reindex database test1;
            reindex table customer_info force;''')
        self.log.info(sql_cmd4)
        self.assertIn(constant.CREATE_DATABASE_SUCCESS, sql_cmd4)
        self.assertIn(constant.REINDEX_SUCCESS_MSG, sql_cmd4)
        self.assertIn(self.res, sql_cmd3)

    def tearDown(self):
        self.log.info('----------this is teardown-------')
        sql_cmd3 = COMMONSH.execut_db_sql('''drop table customer_info;
            drop database if exists test1;''')
        self.log.info(sql_cmd3)
        self.log.info(
            '--------Opengauss_Function_DML_Set_Case0118执行结束----')
