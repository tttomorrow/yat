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
Case Name： 约束相关DDL，创建MOT表，创建约束
Descption:  1.创建普通MOT行存表 2.创建约束 3. 清理数据
'''

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()

class MOT_CONSTRAINT_DDL_TEST(unittest.TestCase):

    def setUp(self):
        logger.info('----------------------------Opengauss_Function_MOT_Case0057开始执行-----------------------------')
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        # logger.info('------------修改配置，并重启数据库------------')
        # self.configitem = "enable_incremental_checkpoint=off"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)

    def test_MOT_CONSTRAINT_DDL(self):
        logger.info('----------------------------开始测试约束定义相关SQL，创建MOT表，创建约束，清理数据-----------------------------')
        self.sql_cmd = f'''
                        --创建有主键约束的MOT表
                        drop foreign table if exists mot_table_test01;
                        create foreign table mot_table_test01(id int primary key,name varchar(10));
                        --指定主键约束的名称
                        drop foreign table if exists mot_table_test02;
                        create foreign table mot_table_test02(id int,name varchar(10),constraint pri_mot_key primary key (id));
                        --创建有非空约束的MOT表
                        drop foreign table if exists mot_table_test03;
                        create foreign table mot_table_test03(id int not null,name varchar(10));
                        --创建有唯一约束的MOT表
                        drop foreign table if exists mot_table_test04;
                        create foreign table mot_table_test04(id int not null unique,name varchar(10));
                        --清理数据
                        drop foreign table mot_table_test01 cascade;
                        drop foreign table mot_table_test02 cascade;
                        drop foreign table mot_table_test03 cascade;
                        drop foreign table mot_table_test04 cascade;
                        '''

        msg = self.sh_primysh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg)
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, msg)

    def tearDown(self):
        # logger.info('----------------------------后置处理-----------------------------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('----------------------------Opengauss_Function_MOT_Case0057执行完成-----------------------------')
