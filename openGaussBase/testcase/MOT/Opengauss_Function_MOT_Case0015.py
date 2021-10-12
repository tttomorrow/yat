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
Case Type： MOT支持的数据类型
Case Name： MOT支持的数据类型smallserial
'''

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

    def test_mot_datatype(self):
        logger.info("-----------------------Opengauss_Function_MOT_Case0015开始执行----------------")
        self.sql_cmd = f'''
                        create schema schema_mot_test;
                        create FOREIGN table schema_mot_test.table01 (name smallserial);
                        insert into schema_mot_test.table01 values (120);
                        select * from schema_mot_test.table01;
                        drop schema schema_mot_test CASCADE;
                                              '''
        logger.info("-------------------------开始用例测试:MOT支持smallserial数据类型--------------------------")
        msg = self.sh_primysh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg)

    def tearDown(self):
        # logger.info('-----------恢复配置，并重启数据库-----------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('---------------Opengauss_Function_MOT_Case0015执行结束---------------')
