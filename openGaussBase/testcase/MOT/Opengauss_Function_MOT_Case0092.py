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
Case Type： MOT支持的DMLs
Case Name： MOT支持INSERT INTO  DELETE FROM
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

    def test_mot_INSERTINTO_DELETEFROM(self):
        logger.info("--------------------Opengauss_Function_MOT_Case0092开始执行------------------")
        self.sql_cmd = f'''
                        CREATE FOREIGN TABLE tableDML1(id int , name VARCHAR(20), tal int, tableid int);
                        CREATE FOREIGN TABLE tableDML2(id int , name VARCHAR(30), tal int, tableid int);
                        INSERT INTO tableDML1(id, name, tal ,tableid) VALUES (1, 'MOT', 12,64);
                        INSERT INTO tableDML2(id, name, tal ,tableid) VALUES (1, 'MOT', 12,64),(2, 'MOTtester', 55,66);
                        DELETE FROM tableDML2 WHERE id = 2;
                        DROP FOREIGN TABLE tableDML1;
                        DROP FOREIGN TABLE tableDML2;   
                      '''
        logger.info("-------------------------开始用例测试:MOT支持的DML--------------------------")
        msg = self.sh_primysh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg)
        self.assertIn(self.constant.DELETE_SUCCESS_MSG, msg)
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, msg)

    def tearDown(self):
        # logger.info('-----------恢复配置，并重启数据库-----------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('---------------Opengauss_Function_MOT_Case0092执行结束---------------')
