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
Case Type： mot不支持DDL
Case Name： mot不支持的DDL，创建as select表
'''

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class Mot_DDL_test(unittest.TestCase):

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

    def test_mot_usddl(self):
        logger.info("------------------------Opengauss_Function_MOT_Case0049开始执行---------------------")
        self.schema = 'schema_mot_test'
        self.sql_cmd = f''' 
                        DROP SCHEMA IF EXISTS {self.schema} CASCADE;
                        CREATE SCHEMA {self.schema};
                        CREATE FOREIGN TABLE {self.schema}.as_tab(a int);
                        --创建as select 表
                        CREATE FOREIGN TABLE as_tab_new as select * from as_tab;
                        DROP SCHEMA {self.schema} CASCADE;
                      '''
        logger.info("-----------------开始用例测试:MOT不支持的DDL，创建as select表----------------------")
        msg = self.sh_primysh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, msg)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg)
        self.assertIn(self.constant.NOT_AS_SELECT, msg)

    def tearDown(self):
        # logger.info('-----------恢复配置，并重启数据库-----------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('---------------Opengauss_Function_MOT_Case0049执行结束---------------')
