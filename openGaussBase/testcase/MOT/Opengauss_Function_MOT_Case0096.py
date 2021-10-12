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
Case Name： 结合MOT表，以START TRANSACTION启动事务并修改隔离级别测试
Descption:  1.开启事务,修改隔离级别和访问模式；2.创建普通MOT行存表； 3.插入数据； 4. 结束事务；5.清理数据；
'''

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()

class MOT_TRANSACTION_TEST(unittest.TestCase):

    def setUp(self):
        logger.info('----------------------------Opengauss_Function_MOT_Case0096开始执行-----------------------------')
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        # logger.info('------------修改配置，并重启数据库------------')
        # self.configitem = "enable_incremental_checkpoint=off"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)

    def test_MOT_Transaction(self):
        logger.info('----------开始测试事务相关SQL，开启事务，修改隔离级别和访问模式，创建MOT表，关闭事务，清理数据------------')
        self.sql_cmd = f'''
                        --开启事务
                        start transaction;
                        --设置当前事务隔离级别为read committed，访问模式为read only
                        set local transaction isolation level read committed read only;
                        --创建MOT表
                        drop foreign table if exists mot_table_test;
                        create foreign table mot_table_test(id int,name varchar(10));
                        --结束事务
                        end;
                        '''

        msg = self.sh_primysh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, msg)
        self.assertIn(self.constant.SET_SUCCESS_MSG, msg)
        self.assertIn('read-only transaction', msg)
        self.assertIn(self.constant.ROLLBACK_MSG, msg)

    def tearDown(self):
        # logger.info('----------------------------后置处理-----------------------------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('----------------------------Opengauss_Function_MOT_Case0096执行完成-----------------------------')
