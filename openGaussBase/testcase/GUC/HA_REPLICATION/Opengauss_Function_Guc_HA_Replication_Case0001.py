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
Case Name   : 使用gs_guc set方法设置参数max_wal_senders为500,观察预期结果
Description :
        1.查询max_wal_senders默认值
        2.修改参数值为500并重启数据库
        3.查询修改后的参数值
        4.恢复参数默认值
Expect      :
        1.显示默认值为16(主备环境一致)
        2.设置成功
        3.查询显示参数值为500
        4.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

commonsh = CommonSH('PrimaryDbUser')


class HAReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Guc_HA_Replication_Case0001start-----')
        self.constant = Constant()
        self.expect_result = '500'

    def test_max_wal_senders(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show max_wal_senders;')
        self.log.info(sql_cmd)
        self.assertEqual('16', sql_cmd.split('\n')[-2].strip())
        self.log.info('--步骤2:修改参数值为500并重启数据库--')
        mod_msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'max_wal_senders =500')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤3:查询修改后的参数值--')
        sql_cmd = commonsh.execut_db_sql('show max_wal_senders;')
        self.log.info(sql_cmd)
        self.assertIn(self.expect_result, sql_cmd)

    def tearDown(self):
        self.log.info('--步骤4:恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('show max_wal_senders;')
        self.log.info(sql_cmd)
        if "16" != sql_cmd.splitlines()[-2].strip():
            mod_msg = commonsh.execute_gsguc('set',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             'max_wal_senders=16')
            self.log.info(mod_msg)
            restart_msg = commonsh.restart_db_cluster()
            self.log.info(restart_msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('show max_wal_senders;')
        self.log.info(sql_cmd)
        self.log.info(
            '--Opengauss_Function_Guc_HA_Replication_Case0001finish----')
