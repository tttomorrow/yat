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
Case Type   : insert--使用default
Case Name   : 给序列型，日期时间型的字段，插入数据，使用default
Description :
    1.建表，指定序列型，日期时间型类型
    2.插入数据，使用default
    3.删表
Expect      :
    1.建表成功
    2.数据插入成功，序列型步长以1递增；时间型显示当前时间
    3.删表成功
History     :
"""
import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class INSERTDEFAULT(unittest.TestCase):

    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Insert_Case0037开始执行-----------------------------')

    def test_insert_default(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists t_insert002;
       CREATE TABLE t_insert002(id SERIAL PRIMARY KEY,time TIMESTAMPTZ NOT NULL DEFAULT now());''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''INSERT INTO t_insert002 values(default,default);
       INSERT INTO t_insert002 values(default,default);
       select * from t_insert002;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)

    def tearDown(self):
        logger.info('-----------this is teardown-----------')
        sql_cmd3 = commonsh.execut_db_sql('''drop table t_insert002;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Insert_Case0037执行结束-----------------------')
