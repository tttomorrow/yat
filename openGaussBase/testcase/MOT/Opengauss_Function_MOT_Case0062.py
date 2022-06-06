"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

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
Case Name： 表定义相关SQL，创建MOT表，插入数据，删除MOT表
Descption:  1.创建普通MOT行存表 2.向MOT表中插入、更新、删除数据 3. 删除MOT行存表
'''

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()

class MOT_TABLE_DDL_TEST(unittest.TestCase):

    def setUp(self):
        logger.info('----------------------------Opengauss_Function_MOT_Case0062开始执行-----------------------------')
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        # logger.info('------------修改配置，并重启数据库------------')
        # self.configitem = "enable_incremental_checkpoint=off"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)

    def test_MOT_table_DDL(self):
        logger.info('--------------------------开始测试表定义相关SQL，创建MOT表，插入数据，删除MOT表--------------------------')
        self.sql_cmd = f'''
                        --创建模式
                        drop schema if exists mot_schema_test;
                        create schema mot_schema_test;
                        --创建普通MOT行存表
                        drop foreign table if exists mot_schema_test.mot_table_test01;
                        drop foreign table if exists mot_schema_test.mot_table_test02;
                        create foreign table mot_schema_test.mot_table_test01(id int,name varchar(10));
                        create foreign table mot_schema_test.mot_table_test02(id int,name varchar(10));
                        --插入数据
                        insert into mot_schema_test.mot_table_test01 values(1,'a');
                        insert into mot_schema_test.mot_table_test01 values(2,'b'),(3,'c'),(4,'d');
                        insert into mot_schema_test.mot_table_test02 select * from mot_schema_test.mot_table_test01;
                        --更新数据
                        update mot_schema_test.mot_table_test01 set name='abc' where id=1;
                        --查看表中数据
                        select * from mot_schema_test.mot_table_test01;
                        --删除表中数据
                        delete from mot_schema_test.mot_table_test01 where id < 2;
                        truncate table mot_schema_test.mot_table_test01;
                        --删除普通MOT行存表 
                        drop foreign table mot_schema_test.mot_table_test01;
                        drop foreign table mot_schema_test.mot_table_test02;
						--删除模式
                        drop schema mot_schema_test cascade;
                        '''

        msg = self.sh_primysh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg)
        self.assertIn(self.constant.UPDATE_SUCCESS_MSG, msg)
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, msg)

    def tearDown(self):
        # logger.info('----------------------------后置处理-----------------------------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('----------------------------Opengauss_Function_MOT_Case0062执行完成-----------------------------')
