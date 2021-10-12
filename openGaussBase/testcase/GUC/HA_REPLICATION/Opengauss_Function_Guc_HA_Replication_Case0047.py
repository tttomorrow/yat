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
Case Type   : GUC
Case Name   : 使用gs_guc set方法设置参数wal_receiver_timeout为7s,观察预期结果
Description :
        1.查询wal_receiver_timeout默认值
        2.修改参数值为7s并重启数据库
        3.恢复参数默认值
Expect      :
        1.显示默认值为6s
        2.设置成功
        3.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class HAReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Guc_HA_Replication_Case0047start-----')
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_wal_receiver_timeout(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show wal_receiver_timeout;')
        self.log.info(sql_cmd)
        self.assertEqual('6s', sql_cmd.split('\n')[2].strip())
        self.log.info('--步骤2:修改参数值为7s并重启数据库--')
        msg = self.commonsh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          'wal_receiver_timeout =7s')
        self.log.info(msg)
        self.assertTrue(msg)
        msg = self.commonsh.restart_db_cluster()
        self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤3:查询修改后的参数值--')
        sql_cmd = self.commonsh.execut_db_sql('show wal_receiver_timeout;')
        self.log.info(sql_cmd)
        self.assertEqual('7s', sql_cmd.split('\n')[2].strip())

    def tearDown(self):
        self.log.info('--步骤4:恢复默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show wal_receiver_timeout;')
        self.log.info(sql_cmd)
        if "6s" != sql_cmd.split('\n')[-2].strip():
            msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              'wal_receiver_timeout=6s')
            self.log.info(msg)
            msg = self.commonsh.restart_db_cluster()
            self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.commonsh.execut_db_sql('show wal_receiver_timeout;')
        self.log.info(sql_cmd)
        self.log.info(
            '--Opengauss_Function_Guc_HA_Replication_Case0047finish----')
