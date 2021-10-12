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
Case Type   : analyze--匿名块
Case Name   : 匿名块中，使用analyze分析表,合理报错
Description :
    1.创建表
    2.匿名块中，使用analyze分析表
    3.删除表
Expect      :
    1.建表成功
    2.合理报错
    3.表删除成功
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0111开始执行-----------------------------')

    def test_analyze(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
       CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER ,WR_RETURNED_TIME_name varchar(200));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 开启匿名块，匿名块中执行analyze语句,合理报错
        sql_cmd2 = commonsh.execut_db_sql('''
       declare
       begin
       analyze verbose customer_info;
       end;
       declare
       begin
       analyze verbose customer_info;
       end;
       declare
       begin
       analyze verbose customer_info(WR_RETURNED_DATE_SK,WR_RETURNED_TIME_name);
       end;''')
        logger.info(sql_cmd2)
        self.assertIn('ERROR:  ANALYZE cannot be executed from a function or multi-command string', sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd3 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0111执行结束--------------------------')
