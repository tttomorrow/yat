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
Case Name： 结合MOT表，与vacuum组合测试
Descption:  1.创建普通MOT行存表；2.插入数据，查看size；3.delete删除数据；4.vacuum回收空间，查看size；5.清理数据；
'''

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()

class MOT_VACUUM_TEST(unittest.TestCase):

    def setUp(self):
        logger.info('----------------------------Opengauss_Function_MOT_Case0100开始执行-----------------------------')
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        # logger.info('------------修改配置，并重启数据库------------')
        # self.configitem = "enable_incremental_checkpoint=off"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)

    def test_MOT_Vacuum(self):
        logger.info('-------------------开始与vacuum组合测试---------------------')
        self.sql_cmd = f'''
                        --创建MOT表
                        drop foreign table if exists mot_table_test;
                        create foreign table mot_table_test(id int,name varchar(10));
                        --插入数据
                        insert into mot_table_test values(generate_series(1,20000),'a');
                        --查看表数据占用大小
                        select pg_size_pretty(pg_relation_size('mot_table_test'));
                        --删除表中数据
                        delete from mot_table_test;
                        --查看表数据占用大小
                        select pg_size_pretty(pg_relation_size('mot_table_test'));
                        --执行vacuum回收空间
                        vacuum full mot_table_test;
                        --查看表数据占用大小
                        select pg_size_pretty(pg_relation_size('mot_table_test'));
                        --清理环境
                        drop foreign table mot_table_test;
                        '''

        msg = self.sh_primysh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg)
        self.assertIn('1304 kB', msg)
        self.assertIn(self.constant.DELETE_SUCCESS_MSG, msg)
        self.assertIn(self.constant.VACUUM_SUCCESS_MSG, msg)
        self.assertIn('8192 bytes', msg)
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, msg)


    def tearDown(self):
        # logger.info('----------------------------后置处理-----------------------------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('----------------------------Opengauss_Function_MOT_Case0100执行完成-----------------------------')
