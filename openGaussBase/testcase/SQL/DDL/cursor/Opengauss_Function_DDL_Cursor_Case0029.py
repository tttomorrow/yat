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
#--  @date:2020/9/15
#--  @testpoint:cursor声明游标，使用value子句，子句类型为不常用数据类型
'''

import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('PrimaryDbUser')
constant = Constant()

class Hostname(unittest.TestCase):


    def setUp(self):
        logger.info("------------------------Opengauss_BaseFunc_DDL_Cursor_0029开始执行--------------------------")

# value子句，类型为不常用数据类型
    def test_pascal(self):
        self.sql_cmd = f'''
                        start transaction;
                        cursor cursor29 for values(hextoraw('DEADBEEF'),area(box '((0,0),(1,1))'),masklen('192.168.1.5/24'));
                        fetch from cursor29;
                        close cursor29;
                        end;
                        '''

        msg = commonsh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(constant.START_TRANSACTION_SUCCESS_MSG, msg)
        self.assertIn(constant.DECLEAR_CURSOR_SUCCESS_MSG, msg)
        self.assertIn('DEADBEEF', msg)
        self.assertIn(constant.CLOSE_CURSOR_SUCCESS_MSG, msg)
        self.assertIn(constant.COMMIT_SUCCESS_MSG, msg)

    def tearDown(self):
        logger.info('No need to clean.')
        logger.info('------------------------Opengauss_BaseFunc_DDL_Cursor_0029执行结束--------------------------')

