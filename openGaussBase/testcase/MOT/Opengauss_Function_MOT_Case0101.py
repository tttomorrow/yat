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
Case Name： 结合MOT表，使用join命令操作表(内联、左联、右联、全外联)
Descption:  1.创建普通MOT行存表；2.插入数据；3.join命令操作；4.清理数据；
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
        logger.info('----------------------------Opengauss_Function_MOT_Case0101开始执行-----------------------------')
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
        logger.info('-------------------开始与join命令组合测试---------------------')
        sql_cmd1 = f'''
                        --创建MOT表
                        drop foreign table if exists mot_table_test1;
                        drop foreign table if exists mot_table_test2;
                        create foreign table mot_table_test1(id int,name varchar(10));
                        create foreign table mot_table_test2(id int,name varchar(10));
                        --插入数据
                        insert into mot_table_test1 values(1,'测试1'),(2,'b'),(3,'测试2'),(4,'d'),(5,'e');
                        insert into mot_table_test2 values(2,'e'),(3,'测试3'),(4,'f'),(5,'l'),(6,'f');
                    '''
        msg1 = self.sh_primysh.execut_db_sql(sql_cmd1)
        logger.info(msg1)

        sql_cmd2 = f'''
                        --left join左连接
                        select t1.name name from mot_table_test1 t1 left join mot_table_test2 t2 on t1.id=t2.id;
                    '''
        msg2 = self.sh_primysh.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn('测试1', msg2)

        sql_cmd3 = f'''
                        --right join右连接
                        select t1.name name from mot_table_test1 t1 right join mot_table_test2 t2 on t1.id=t2.id;
                    '''
        msg3 = self.sh_primysh.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        self.assertIn('测试2', msg3)

        sql_cmd4 = f'''
                        --join内连接
                        select t1.name name from mot_table_test1 t1 join mot_table_test2 t2 on t1.id=t2.id;
                    '''
        msg4 = self.sh_primysh.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        self.assertIn('测试2', msg4)

        sql_cmd5 = f'''
                        --清理环境
                        drop foreign table mot_table_test1;
                        drop foreign table mot_table_test2;
                    '''
        msg5 = self.sh_primysh.execut_db_sql(sql_cmd5)
        logger.info(msg5)
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, msg5)


    def tearDown(self):
        # logger.info('----------------------------后置处理-----------------------------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('----------------------------Opengauss_Function_MOT_Case0101执行完成-----------------------------')
