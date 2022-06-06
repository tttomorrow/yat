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
Case Name   : 使用gs_guc set方法设置参数enable_slot_log为on,观察预期结果
Description :
        1.查询enable_slot_log默认值
        2.修改参数wal_level为logical
        3.在主机创建逻辑复制槽并查询
        4.备机查询逻辑复制槽信息
        5.修改参数enable_slot_log为on
        6.在主机创建逻辑复制槽并查询
        7.备机查询逻辑复制槽信息
        8.删除逻辑复制槽
        9.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.修改成功
        3.创建成功
        4.备机查询无信息，未同步
        5.修改成功
        6.创建成功
        7.查询成功，主备开启逻辑复制槽主备同步特性
        8.删除成功
        9.默认值恢复成功
History     :
"""
import unittest
import os
import time

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class HAReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-----Opengauss_Function_Guc_HA_Replication_Case0007start-----')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.conf_path = os.path.join(macro.DB_INSTANCE_PATH,
                                      macro.DB_PG_CONFIG_NAME)

    def test_enable_slot_log(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = Primary_SH.execut_db_sql('show enable_slot_log;')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        self.log.info('--步骤2:修改参数wal_level为logical后创建逻辑复制槽--')
        msg = Primary_SH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       'wal_level =logical')
        self.log.info(msg)
        self.assertTrue(msg)
        self.log.info('--步骤3:重启数据库--')
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤4:查询修改后的参数值--')
        sql_cmd = Primary_SH.execut_db_sql('show wal_level;')
        self.log.info(sql_cmd)
        self.assertIn('logical', sql_cmd)
        self.log.info('--步骤5:主机创建逻辑复制槽--')
        sql_cmd = "select * from pg_create_logical_replication_slot" \
                  "('365slot', 'mppdb_decoding');"
        excute_cmd = f'source {self.DB_ENV_PATH};' \
                     f'gsql -d {self.primary_node.db_name}' \
                     f' -p {self.primary_node.db_port}' \
                     f' -c "{sql_cmd}"'
        self.log.info(excute_cmd)
        msg = self.primary_node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn('365slot', msg)
        self.log.info('--步骤6:主机查询逻辑复制槽--')
        sql_cmd = "select slot_name,plugin from pg_get_replication_slots();"
        excute_cmd = f'source {self.DB_ENV_PATH};' \
                     f'gsql -d {self.primary_node.db_name}' \
                     f' -p {self.primary_node.db_port}' \
                     f' -c "{sql_cmd}"'
        self.log.info(excute_cmd)
        msg = self.primary_node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn('365slot', msg)
        self.log.info('--步骤7:备机查询逻辑复制槽，无信息--')
        sql_cmd = "select slot_name,plugin from pg_get_replication_slots();"
        excute_cmd = f'source {self.DB_ENV_PATH};' \
                     f' gsql -d {self.standby_node.db_name}' \
                     f' -p {self.standby_node.db_port}' \
                     f' -c "{sql_cmd}"'
        self.log.info(excute_cmd)
        msg = self.standby_node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn('', msg)
        self.log.info('--步骤8:修改参数值为on并重启数据库--')
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'enable_slot_log =on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤9:查询修改后的参数值--')
        sql_cmd = Primary_SH.execut_db_sql('show enable_slot_log;')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)
        self.log.info('--步骤10:查询节点信息--')
        get_pgxc_node_name_cmd = f"cat {self.conf_path}|" \
                                 f"grep 'pgxc_node_name'|" \
                                 f"cut -d \"'\" -f 2"
        self.log.info(get_pgxc_node_name_cmd)
        pgxc_node_name = self.primary_node.sh(get_pgxc_node_name_cmd).result()
        self.log.info(pgxc_node_name)
        self.assertIsNotNone(pgxc_node_name)
        node_num = len(pgxc_node_name.strip('dn_').split('_'))
        self.log.info('----步骤11:查看主机query，同步是否正常----')
        Primary_SH.check_location_consistency('primary', node_num)
        self.log.info('----步骤12:查询主备状态----')
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤13:主机查询逻辑复制槽--')
        sql_cmd = "select * from pg_create_logical_replication_slot" \
                  "('365slot1', 'mppdb_decoding');"
        excute_cmd = f'source {self.DB_ENV_PATH};' \
                     f' gsql -d {self.primary_node.db_name}' \
                     f' -p {self.primary_node.db_port}' \
                     f' -c "{sql_cmd}"'
        self.log.info(excute_cmd)
        msg = self.primary_node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn('365slot1', msg)
        time.sleep(5)
        self.log.info('--步骤14:备机查询，查询成功，有数据--')
        sql_cmd = "select slot_name,plugin from pg_get_replication_slots();"
        excute_cmd = f'source {self.DB_ENV_PATH};' \
                     f' gsql -d {self.standby_node.db_name}' \
                     f' -p {self.standby_node.db_port}' \
                     f' -c "{sql_cmd}"'
        self.log.info(excute_cmd)
        msg = self.standby_node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn('365slot1', msg)

    def tearDown(self):
        self.log.info('--步骤15:清理环境--')
        sql_cmd = Primary_SH.execut_db_sql("select * from"
                                           " pg_drop_replication_slot"
                                           "('365slot');"
                                           "select * from"
                                           " pg_drop_replication_slot"
                                           "('365slot1');")
        self.log.info(sql_cmd)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'enable_slot_log=off')
        self.log.info(mod_msg)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = Primary_SH.execut_db_sql('show enable_slot_log;')
        self.log.info(sql_cmd)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'wal_level=hot_standby')
        self.log.info(mod_msg)
        msg = Primary_SH.restart_db_cluster()
        self.log.info(msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = Primary_SH.execut_db_sql('show wal_level;')
        self.log.info(sql_cmd)
        self.log.info(
            '--Opengauss_Function_Guc_HA_Replication_Case0007finish----')
