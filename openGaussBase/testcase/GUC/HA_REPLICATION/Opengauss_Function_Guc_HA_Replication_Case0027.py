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
Case Type   : GUC
Case Name   : 使用gs_guc set方法设置参数enable_data_replicate为on,
             观察预期结果
Description :
        1.查询enable_data_replicate默认值
        2.修改参数值为on并重启数据库
        3.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.设置成功，查询显示仍然是off，当replication_type参数为1时，
        不允许设置为on，如果此时用guc工具设置成on，会强制改为off
        3.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

constant = Constant()


class HAReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Guc_HA_Replication_Case0027start-----')
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_enable_data_replicate(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show enable_data_replicate;')
        self.log.info(sql_cmd)
        self.assertIn(constant.BOOLEAN_VALUES[1], sql_cmd)
        self.log.info('--步骤2: 查询replication_type参数值--')
        sql_cmd = self.commonsh.execut_db_sql('show replication_type;')
        self.log.info(sql_cmd)
        self.assertIn('1', sql_cmd)
        self.log.info('--步骤3:修改参数值为on并重启数据库--')
        mod_msg = self.commonsh.execute_gsguc('set',
                                              constant.GSGUC_SUCCESS_MSG,
                                              'enable_data_replicate =on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = self.commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤3:查询修改后的参数值--')
        sql_cmd = self.commonsh.execut_db_sql('show enable_data_replicate;')
        self.log.info(sql_cmd)
        self.assertIn(constant.BOOLEAN_VALUES[1], sql_cmd)

    def tearDown(self):
        self.log.info('--步骤4:恢复默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show enable_data_replicate;')
        self.log.info(sql_cmd)
        if "off" != sql_cmd.split('\n')[-2].strip():
            mod_msg = self.commonsh.execute_gsguc('set',
                                                  constant.GSGUC_SUCCESS_MSG,
                                                  'enable_data_replicate=off')
            self.log.info(mod_msg)
            restart_msg = self.commonsh.restart_db_cluster()
            self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.commonsh.execut_db_sql('show enable_data_replicate;')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_Guc_HA_Replication_Case0027finish---')
