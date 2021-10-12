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
Case Name   : MOT表不支持jsonb类型
Description :
    1. 创建表,包含列的类型为jsonb
Expect      :
    1. 创建失败
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class Jsonb(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.configitem = "enable_incremental_checkpoint=off"
        msg1 = self.primysh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          self.configitem)
        self.log.info(msg1)
        stopmsg = str(self.primysh.stop_db_cluster())
        startmsg = str(self.primysh.start_db_cluster())
        self.assertTrue(stopmsg)
        self.assertTrue(startmsg)

    def test_mot_none_datatype_array(self):
        self.log.info("---Opengauss_Function_MOT_Case0142开始执行---")
        self.schema = 'schema_mot_test'
        self.tablename = 'MOTTable'
        self.datatype = 'jsonb'
        self.sql_cmd = f'''CREATE SCHEMA {self.schema};
            CREATE FOREIGN TABLE {self.schema}.{self.tablename}\
            (t1 {self.datatype});
            DROP SCHEMA {self.schema} CASCADE;
            '''
        self.log.info("----开始用例测试:MOT不支持数据类型jsonb----")
        msg2 = self.primysh.execut_db_sql(self.sql_cmd)
        self.log.info(msg2)
        self.assertIn(self.constant.NOT_SUPPORTED_TYPE, msg2)

    def tearDown(self):
        self.log.info('-----------恢复配置，并重启数据库-----------')
        self.configitem = "enable_incremental_checkpoint=on"
        msg3 = self.primysh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          self.configitem)
        self.log.info(msg3)
        stopmsg = str(self.primysh.stop_db_cluster())
        startmsg = str(self.primysh.start_db_cluster())
        self.assertTrue(stopmsg)
        self.assertTrue(startmsg)
        self.log.info('------Opengauss_Function_MOT_Case0142执行结束-----')
