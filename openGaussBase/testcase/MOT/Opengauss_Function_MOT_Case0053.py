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
Case Name： MOT不支持Merge into
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

    def test_mot_Mergeinto(self):
        logger.info("----------------------Opengauss_Function_MOT_Case0053开始执行--------------------")
        self.sql_cmd = f'''
                        create schema schema_mot_test;
                        CREATE FOREIGN TABLE schema_mot_test.products (product_id INTEGER, product_name VARCHAR2(60), category VARCHAR2(60));
                        INSERT INTO schema_mot_test.products VALUES (1502, 'olympus camera', 'electrncs'),(1601, 'lamaze', 'toys'),(1666, 'harry potter', 'toys'),(1700, 'wait interface', 'books'); 
                        CREATE FOREIGN TABLE schema_mot_test.newproducts (product_id INTEGER, product_name VARCHAR2(60), category VARCHAR2(60)); 
                        INSERT INTO schema_mot_test.newproducts VALUES (1501, 'vivitar 35mm', 'electrncs'),(1502, 'olympus ', 'electrncs'),(1600, 'play gym', 'toys'),(1601, 'lamaze', 'toys'), (1666, 'harry potter', 'dvd'); 
                        MERGE INTO schema_mot_test.newproducts np  USING schema_mot_test.products p ON (np.product_id = p.product_id ) WHEN MATCHED THEN UPDATE SET np.product_name = p.product_name, np.category = p.category WHEN NOT MATCHED THEN  INSERT VALUES (p.product_id, p.product_name, p.category) ; 
                        DROP SCHEMA schema_mot_test CASCADE;        
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
        logger.info('---------------Opengauss_Function_MOT_Case0053执行结束---------------')


