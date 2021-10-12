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
"""
Case Type   : 功能测试
Case Name   : MOT支持的DDL，update from
Description :
    1.设置enable_incremental_checkpoint参数为off,并重启数据库;
    2.创建内存表，插入数据，结合update from语句，验证支持的DDL，查看执行结果，清理环境，删除内存表；
    3.恢复环境默认配置，修改enable_incremental_checkpoint为on，并重启数据库；
Expect      :
    1.设置成功，重启数据库成功；
    2.创建内存表成功，插入数据成功，执行update from语句成功，查看执行结果成功，清理环境成功；
    3.修改参数成功，重启数据库成功；
History     : 
"""

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class Mot_datatype_test(unittest.TestCase):

    def setUp(self):
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        # logger.info('------------修改配置，并重启数据库------------')
        # self.configitem = "enable_incremental_checkpoint=off"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)

    def test_mot_constraint(self):
        logger.info("------------------------Opengauss_Function_MOT_Case0056开始执行----------------------")
        self.sql_cmd = f'''
                        drop foreign table if exists mot_dml_test1;
                        drop foreign table if exists mot_dml_test2;
                        create foreign table mot_dml_test1(id1 int,name1 varchar(10));
                        create foreign table mot_dml_test2(id2 int,name2 varchar(10));
                        insert into mot_dml_test1 values(1,'a'),(2,'b'),(3,'c'),(4,'d'),(5,'e');
                        insert into mot_dml_test2 values(3,'a'),(4,'b'),(5,'c'),(6,'d'),(7,'e');
                        select * from mot_dml_test1;
                        select * from mot_dml_test2;
                        update mot_dml_test2 t2 set name2=char_length(name1) from mot_dml_test1 t1 where t1.id1=t2.id2;
                        select * from mot_dml_test2;
                        drop foreign table mot_dml_test1;
                        drop foreign table mot_dml_test2;
                      '''
        logger.info("-------------------------开始用例测试:MOT支持的DML,update from--------------------------")
        msg = self.sh_primysh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg)
        self.assertIn(self.constant.UPDATE_SUCCESS_MSG, msg)
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, msg)

    def tearDown(self):
        logger.info('-----------恢复配置，并重启数据库-----------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('-------------------Opengauss_Function_MOT_Case0056执行结束----------------------')
