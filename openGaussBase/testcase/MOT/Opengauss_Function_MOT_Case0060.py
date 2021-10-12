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
Case Name： 索引定义相关SQL，创建MOT表，创建索引
Descption:  1.创建普通MOT表 2.创建普通索引、唯一索引、指定索引、重命名索引等 3. 删除索引、清理数据
'''

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


logger = Logger()

class MOT_INDEX_DDL_TEST(unittest.TestCase):

    def setUp(self):
        logger.info('----------------------------Opengauss_Function_MOT_Case0060开始执行-----------------------------')
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        # logger.info('------------修改配置，并重启数据库------------')
        # self.configitem = "enable_incremental_checkpoint=off"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)

    def test_mot_index_DDL(self):
        logger.info('-----------------开始测试索引定义相关SQL，创建MOT表，创建唯一索引、指定索引等，删除索引、清理数据-------------------')
        self.sql_cmd = f'''
                            --创建MOT表（非空）
                            drop foreign table if exists mot_table_test;
                            create foreign table mot_table_test(id int not null,name varchar(10) not null);
                            --创建普通索引
                            create index id_index1 on mot_table_test(id);
                            --创建唯一索引
                            create unique index id_index2 on mot_table_test(id);
                            --创建指定索引
                            create index id_index3 on mot_table_test using btree(id);
                            --单表创建小于等于9个的索引
                            create index id_index4 on mot_table_test(id);
                            create index id_index5 on mot_table_test(id);
                            create index id_index6 on mot_table_test(id);
                            create index id_index7 on mot_table_test(id);
                            create index id_index8 on mot_table_test(id);
                            create index id_index9 on mot_table_test(id);
                            --重命名已有索引
                            alter index id_index1 rename to id_index_new;
                            --设置索引不可用
                            alter index id_index2 unusable;
                            --删除索引
                            drop index id_index3;
                            --清理数据
                            drop foreign table mot_table_test;
                            '''

        msg = self.sh_primysh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS, msg)
        self.assertIn(self.constant.ALTER_INDEX_SUCCESS_MSG, msg)
        self.assertIn(self.constant.DROP_INDEX_SUCCESS_MSG, msg)

    def tearDown(self):
        # logger.info('----------------------------后置处理-----------------------------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('----------------------------Opengauss_Function_MOT_Case0060执行完成-----------------------------')
