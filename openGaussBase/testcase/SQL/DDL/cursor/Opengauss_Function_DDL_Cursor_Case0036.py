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
--  testpoint:declare声明游标，以默认方式（自动判断）检索数据行，参数设为scroll，合理报错；
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
        logger.info("------------------Opengauss_Function_DDL_Cursor_Case0036开始执行-----------------")
        logger.info("======前置条件，创建表======")
        sql_cmd1 = f'''
                    drop table if exists cur_test_36;
                    create table cur_test_36(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
                    insert into cur_test_36 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                    (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                    (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');
                    '''
        msg1 = self.sh_primysh.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg1)

        logger.info("======以默认方式检索数据行，参数为scroll======")
        sql_cmd2 = f'''
                    start transaction;
                    declare cursor36 scroll cursor for select * from cur_test_36 order by 1;
                    fetch from cursor36;
                    close cursor36;
                    end;
                    '''

        msg2 = self.sh_primysh.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, msg2)
        self.assertIn('SCROLL CURSOR is not yet supported', msg2)
        self.assertIn('current transaction is aborted, commands ignored until end of transaction block', msg2)
        self.assertIn(self.constant.ROLLBACK_MSG, msg2)

    def tearDown(self):
        logger.info('======清理环境======')
        sql_cmd3 = f'''
                    drop table cur_test_36 cascade;
                   '''
        msg3 = self.sh_primysh.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        logger.info('---------------Opengauss_Function_DDL_Cursor_Case0036执行结束---------------')





