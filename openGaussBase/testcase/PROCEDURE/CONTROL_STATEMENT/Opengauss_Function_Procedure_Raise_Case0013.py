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
Case Type   : PROCEDURE
Case Name   : 存储过程中调试语句  SQLSTATE
Description :
    1.创建存储过程
    2.调用存储过程
    3.删除存储过程
Expect      :
    1.创建存储过程成功
    2.调用存储过程成功
    3.删除存储过程成功
History     :
"""
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()
class Hostname(unittest.TestCase):
    def setUp(self):
         logger.info("------------------------ Opengauss_Function_Procedure_Raise_Case0013 开始执行--------------------------")
    def test_before_1(self):
        logger.info("------------------------创建存储过程--------------------------")
        SqlMdg = commonsh.execut_db_sql('''CREATE OR REPLACE PROCEDURE proc_raise2(user_id in integer)
                                        AS
                                        BEGIN
                                            RAISE unique_violation USING MESSAGE = 'Duplicate user ID: ' || user_id;
                                        END;
                                        ''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_PROCEDURE_SUCCESS_MSG, SqlMdg)
        SqlMdg = commonsh.execut_db_sql('''\set VERBOSITY verbose''')
        logger.info(SqlMdg)
        logger.info("------------------------调用存储过程--------------------------")
        SqlMdg = commonsh.execut_db_sql('''call proc_raise2(300011);''')
        logger.info(SqlMdg)
        self.assertIn('Duplicate user ID: 300011', SqlMdg)
    def tearDown(self):
         logger.info('------------------------ Opengauss_Function_Procedure_Raise_Case0013 执行结束--------------------------')
         SqlMdg = commonsh.execut_db_sql('''drop  PROCEDURE proc_raise2;''')
         logger.info(SqlMdg)
         self.assertIn(constant.DROP_PROCEDURE_SUCCESS_MSG, SqlMdg)