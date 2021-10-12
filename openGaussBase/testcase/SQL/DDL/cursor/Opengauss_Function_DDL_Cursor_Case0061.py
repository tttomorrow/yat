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
--  testpoint:declare声明游标，同一事务中定义多个同名游标，合理报错；
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
        logger.info("------------------Opengauss_Function_DDL_Cursor_Case0061开始执行-----------------")
        logger.info("======前置条件，创建表,插入数据======")
        sql_cmd1 = f'''
                    drop table if exists cur_test_61;
                    create table cur_test_61(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
                    insert into cur_test_61 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                    (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                    (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

                    '''
        msg1 = self.sh_primysh.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg1)

        logger.info("======同一事务中定义多个同名游标======")
        sql_cmd2 = f'''
                    start transaction;
                    declare cursor61 cursor for select * from cur_test_61 order by 1;
                    declare cursor61 cursor for select * from cur_test_61 order by 1;
                    declare cursor61 cursor for select * from cur_test_61 order by 1;
                    fetch from cursor61;
                    close cursor61;
                    commit;
                    '''

        msg2 = self.sh_primysh.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, msg2)
        self.assertIn(self.constant.DECLEAR_CURSOR_SUCCESS_MSG, msg2)
        self.assertIn('already exists', msg2)
        self.assertIn('current transaction is aborted, commands ignored until end of transaction block', msg2)
        self.assertIn(self.constant.ROLLBACK_MSG, msg2)

    def tearDown(self):
        logger.info('======清理环境======')
        sql_cmd3 = f'''
                    drop table cur_test_61 cascade;
                   '''
        msg3 = self.sh_primysh.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        logger.info('---------------Opengauss_Function_DDL_Cursor_Case0061执行结束---------------')


