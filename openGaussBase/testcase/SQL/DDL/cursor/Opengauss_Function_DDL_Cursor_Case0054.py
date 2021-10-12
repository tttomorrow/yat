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
--  testpoint:declare声明游标，使用value子句，子句类型为日期/时间类型；
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
        logger.info("------------------Opengauss_Function_DDL_Cursor_Case0054开始执行-----------------")
        logger.info("======结合value子句，子句类型为日期/时间类型======")
        sql_cmd = f'''
                    start transaction;
                    declare cursor54 cursor for values(date '08-12-2020',time without time zone '16:38:22',time with time zone '16:40:40 pst',
                    timestamp without time zone '2020-08-12',timestamp with time zone '2020-08-12 pst',smalldatetime '2020-08-12 16:40:06');
                    fetch forward 6 from cursor54;
                    close cursor54;
                    end;
                    '''
        msg = self.sh_primysh.execut_db_sql(sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, msg)
        self.assertIn(self.constant.DECLEAR_CURSOR_SUCCESS_MSG, msg)
        self.assertIn('2020-08-12 00:00:00', msg)
        self.assertIn(self.constant.CLOSE_CURSOR_SUCCESS_MSG, msg)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, msg)


    def tearDown(self):
        logger.info('======No need to clean======')
        logger.info('---------------Opengauss_Function_DDL_Cursor_Case0054执行结束---------------')


