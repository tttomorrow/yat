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
--  testpoint:declare声明游标，验证事务结束后游标是否能继续使用，参数设为with hold，事务结束后游标仍可使用；
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
        logger.info("------------------Opengauss_Function_DDL_Cursor_Case0040开始执行-----------------")
        logger.info("======前置条件，创建表======")
        sql_cmd1 = f'''
                    drop table if exists cur_test_40;
                    create table cur_test_40(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
                    insert into cur_test_40 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                    (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                    (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');
                    '''
        msg1 = self.sh_primysh.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg1)

        logger.info("======验证事务结束后游标是否能继续使用，参数设为with hold======")
        sql_cmd2 = f'''
                    start transaction;
                    declare cursor40 cursor with hold for select * from cur_test_40 order by 1;
                    fetch from cursor40;
                    end;
                    
                    --继续提取数据，成功
                    fetch from cursor40;
                    close cursor40;
                    '''

        msg2 = self.sh_primysh.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, msg2)
        self.assertIn(self.constant.DECLEAR_CURSOR_SUCCESS_MSG, msg2)
        self.assertIn('Beijing', msg2)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, msg2)
        self.assertIn('Shanghai', msg2)
        self.assertIn(self.constant.CLOSE_CURSOR_SUCCESS_MSG, msg2)

    def tearDown(self):
        logger.info('======清理环境======')
        sql_cmd3 = f'''
                    drop table cur_test_40 cascade;
                   '''
        msg3 = self.sh_primysh.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        logger.info('---------------Opengauss_Function_DDL_Cursor_Case0040执行结束---------------')


