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
Case Name   : 使用gs_guc set方法设置参数wal_receiver_buffer_size为无效值,
              合理报错
Description :
        1.查询wal_receiver_buffer_size默认值
        2.修改参数值为字符test
        3.修改参数值为4095
        4.修改参数值为空串
        5.修改参数值为4098.55
        6.修改参数值为1047553
        7.恢复参数默认值
Expect      :
        1.显示默认值为64MB
        2.合理报错
        3.合理报错
        4.合理报错
        5.合理报错
        6.合理报错
        7.默认值恢复成功
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
            '--Opengauss_Function_Guc_HA_Replication_Case0054start----')
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_wal_receiver_buffer_size(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show '
                                              'wal_receiver_buffer_size;')
        self.log.info(sql_cmd)
        self.assertEqual('64MB', sql_cmd.split('\n')[2].strip())
        self.log.info('--步骤2:修改参数值test, 4095,"''",4098.55,1047553')
        invalid_value = ['test', 4095, "''", 4098.55, 1047553]
        for i in invalid_value:
            result = self.commonsh.execute_gsguc("set",
                                                 constant.GSGUC_SUCCESS_MSG,
                                                 f"'wal_receiver_buffer_size"
                                                 f"={i}")
            self.assertFalse(result)

    def tearDown(self):
        self.log.info('--步骤3:恢复默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show'
                                              ' wal_receiver_buffer_size;')
        self.log.info(sql_cmd)
        if "64MB" != sql_cmd.split('\n')[-2].strip():
            mod_msg = self.commonsh.execute_gsguc('set',
                                                  constant.GSGUC_SUCCESS_MSG,
                                                  'wal_receiver_buffer_size'
                                                  '=64MB')
            self.log.info(mod_msg)
            restart_msg = self.commonsh.restart_db_cluster()
            self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.commonsh.execut_db_sql('show'
                                              ' wal_receiver_buffer_size;')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_Guc_HA_Replication_Case0054执行完成-----')
