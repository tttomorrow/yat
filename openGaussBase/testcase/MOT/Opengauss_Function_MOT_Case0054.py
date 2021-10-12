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
Case Type： MOT不支持的DML
Case Name： MOT不支持列约束
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

    def test_mot_constraint(self):
        logger.info("------------------------Opengauss_Function_MOT_Case0054开始执行---------------------")
        self.sql_cmd = f'''
                        create schema schema_mot_test;
                        CREATE foreign TABLE schema_mot_test.warehouse_t20
                        (
                            W_WAREHOUSE_SK            INTEGER               PRIMARY KEY,                 
                            W_WAREHOUSE_ID            CHAR(16)              NOT NULL,
                            W_WAREHOUSE_NAME          VARCHAR(20)           CHECK (W_WAREHOUSE_NAME IS NOT NULL),
                            W_WAREHOUSE_SQ_FT         INTEGER                       ,
                            W_STREET_NUMBER           CHAR(10)                      ,
                            W_STREET_NAME             VARCHAR(60)                   ,
                            W_STREET_TYPE             CHAR(15)                      ,
                            W_SUITE_NUMBER            CHAR(10)                      ,
                            W_CITY                    VARCHAR(60)                   ,
                            W_COUNTY                  VARCHAR(30)                   ,
                            W_STATE                   CHAR(2)                       ,
                            W_ZIP                     CHAR(10)                      ,
                            W_COUNTRY                 VARCHAR(20)                   ,
                            W_GMT_OFFSET              DECIMAL(5,2),
                            CONSTRAINT W_CONSTR_KEY2 CHECK(W_WAREHOUSE_SK > 0 AND W_WAREHOUSE_NAME IS NOT NULL) 
                        );
                        drop schema schema_mot_test CASCADE;      
                      '''
        logger.info("-------------------------开始用例测试:MOT不支持的DML--------------------------")
        msg = self.sh_primysh.execut_db_sql(self.sql_cmd)
        logger.info(msg)
        self.assertIn(self.constant.NOT_SUPPORTED_TYPE, msg)

    def tearDown(self):
        # logger.info('-----------恢复配置，并重启数据库-----------')
        # self.configitem = "enable_incremental_checkpoint=on"
        # mod_msg = self.sh_primysh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG, self.configitem)
        # stopmsg = str(self.sh_primysh.stop_db_cluster())
        # startmsg = str(self.sh_primysh.start_db_cluster())
        # self.assertTrue(stopmsg)
        # self.assertTrue(startmsg)
        logger.info('---------------Opengauss_Function_MOT_Case0054执行结束---------------')
