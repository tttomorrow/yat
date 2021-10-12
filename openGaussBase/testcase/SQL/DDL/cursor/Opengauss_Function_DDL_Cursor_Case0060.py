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
'''
--  Case Type:Cursor
--  testpoint:declare声明游标，使用value子句，子句类型为不常用数据混合数据类型；
--  date:2020-11-03
'''

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class CURSOR_TEST(unittest.TestCase):

    def setUp(self):
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()

    def test_cursor_declare(self):
        logger.info("------------------Opengauss_Function_DDL_Cursor_Case0060开始执行-----------------")
        logger.info("======结合value子句，子句类型为不常用数据混合数据类型======")
        sql_cmd = f'''
                    start transaction;
                    declare cursor60 cursor for values(HEXTORAW('DEADBEEF'),area(box '((0,0),(1,1))'),masklen('192.168.1.5/24'));
                    fetch from cursor60;
                    close cursor60;
                    end;
                    '''
        msg = self.sh_primysh.execut_db_sql(sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, msg)
        self.assertIn(self.constant.DECLEAR_CURSOR_SUCCESS_MSG, msg)
        self.assertIn('DEADBEEF', msg)
        self.assertIn(self.constant.CLOSE_CURSOR_SUCCESS_MSG, msg)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, msg)


    def tearDown(self):
        logger.info('======No need to clean======')
        logger.info('---------------Opengauss_Function_DDL_Cursor_Case0060执行结束---------------')


