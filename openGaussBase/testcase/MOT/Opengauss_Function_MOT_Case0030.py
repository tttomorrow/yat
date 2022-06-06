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
"""
Case Type   : 功能测试
Case Name   : MOT不支持的数据类型，hstore
Description :
    1.设置enable_incremental_checkpoint参数为off,并重启数据库;
    2.创建内存表，字段类型为hstore，插入数据，查看执行结果，清理环境，删除内存表；
    3.恢复环境默认配置，修改enable_incremental_checkpoint为on，并重启数据库；
Expect      :
    1.设置成功，重启数据库成功；
    2.创建内存表失败，清理环境成功；
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

    def test_mot_none_datatype_array(self):
        logger.info("------------------------Opengauss_Function_MOT_Case0030开始执行------------------")
        self.schema = 'schema_mot_test'
        self.tablename = 'MOTTable'
        self.datatype = 'hstore'
        self.sql_cmd = f'''CREATE SCHEMA {self.schema};
                      CREATE FOREIGN TABLE {self.schema}.{self.tablename}(t1 {self.datatype});
                      DROP SCHEMA {self.schema} CASCADE;
                      '''
        logger.info("-------------------------开始用例测试:MOT不支持数据类型hstore--------------------------")
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
        logger.info('---------------Opengauss_Function_MOT_Case0030执行结束---------------')
