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
Case Type： MOT
Case Name： 结合MOT表，游标相关DDL
Descption:  1.创建普通MOT行存表 2.创建存储过程，定义游标 3. 清理数据
'''

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()

class MOT_CURSOR_DDL_TEST(unittest.TestCase):

    def setUp(self):
        logger.info('----------------------------Opengauss_Function_MOT_Case0058开始执行-----------------------------')
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        # logger.info('------------修改配置，并重启数据库------------')
        # self.configitem = "enable_incremental_checkpoint=off"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)

    def test_MOT_CURSOR_DDL(self):
        logger.info('----------------------------开始测试游标定义相关SQL，创建MOT表，定义游标，清理数据-----------------------------')
        self.sql_cmd1 = f'''
                        --创建MOT表
                        drop foreign table if exists mot_table_test;
                        create foreign table mot_table_test(id int,name varchar(10));
                        '''
        self.sql_cmd2 = f'''
                        --创建存储过程，定义游标
                        drop procedure if exists cursor_mot_test;
                        create or replace procedure cursor_mot_test()
                        as
                        declare
                            type cursor_type is ref cursor;
                            C1 cursor_type;
                            sql_str varchar(100);
                            C2 varchar;
                        begin
                            for i in 0..10 loop
                                insert into mot_table_test values(i,i||'a');
                            end loop;
                            sql_str := 'select name from mot_table_test where id=6;';
                            execute immediate sql_str;
                            open C1 for sql_str;
                            fetch C1 into C2;
                            raise info 'output:%',C2;
                            close C1;
                        end;
                        '''
        self.sql_cmd3 = f'''
                        call cursor_mot_test();
                        --清理数据
                        drop procedure cursor_mot_test;
                        drop foreign table  mot_table_test;
                        '''

        msg1 = self.sh_primysh.execut_db_sql(self.sql_cmd1)
        msg2 = self.sh_primysh.execut_db_sql(self.sql_cmd2)
        msg3 = self.sh_primysh.execut_db_sql(self.sql_cmd3)
        logger.info(msg1)
        logger.info(msg2)
        logger.info(msg3)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg1)
        self.assertIn(self.constant.CREATE_PROCEDURE_SUCCESS_MSG, msg2)
        self.assertIn(self.constant.DROP_PROCEDURE_SUCCESS_MSG, msg3)

    def tearDown(self):
        # logger.info('----------------------------后置处理-----------------------------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('----------------------------Opengauss_Function_MOT_Case0058执行完成-----------------------------')
