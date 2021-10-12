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
Case Name： 结合MOT表，视图相关DDL
Descption:  1.创建普通MOT行存表 2.创建视图，查看视图 3. 清理数据
'''

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()

class MOT_VIEW_DDL_TEST(unittest.TestCase):

    def setUp(self):
        logger.info('----------------------------Opengauss_Function_MOT_Case0090开始执行-----------------------------')
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        # logger.info('------------修改配置，并重启数据库------------')
        # self.configitem = "enable_incremental_checkpoint=off"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)

    def test_MOT_VIEW_DDL(self):
        logger.info('----------------------------开始测试视图相关SQL，创建MOT表，创建视图，清理数据-----------------------------')
        self.sql_cmd = f'''
                        --创建MOT表
                        drop foreign table if exists mot_table_test;
                        create foreign table mot_table_test(id int,name varchar(10));
                        --插入数据
                        insert into mot_table_test values(1,'a');
                        insert into mot_table_test values(3,'b');
                        insert into mot_table_test values(5,'c');
                        insert into mot_table_test values(7,'d');
                        insert into mot_table_test values(9,'e');
                        --创建视图
                        create view mot_view as select * from mot_table_test where id < 6;
                        --查看视图
                        select * from mot_view;
                        --清理数据
                        drop foreign table mot_table_test cascade;
                        '''

        msg = self.sh_primysh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg)
        self.assertIn(self.constant.CREATE_VIEW_SUCCESS_MSG, msg)
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, msg)

    def tearDown(self):
        # logger.info('----------------------------后置处理-----------------------------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('----------------------------Opengauss_Function_MOT_Case0090执行完成-----------------------------')
