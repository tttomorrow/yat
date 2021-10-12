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
Case Type   : 逻辑复制
Case Name   : 用户没有replication权限，主机创建逻辑复制槽，合理报错
Description :
        1.修改参数wal_level为logical;enable_slot_log为on
        2.重启数据库
        3.主机创建逻辑复制槽
        4.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.重启数据库成功
        3.合理报错
        4.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '--Opengauss_Function_Standby_Logical_Replication_Case0003start-')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)

    def test_standby_logical(self):
        self.log.info('--步骤1:修改wal_level为logical;enable_slot_log为on--')
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'wal_level =logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'enable_slot_log =on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        self.log.info('--步骤2:重启数据库--')
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤3:主机创建逻辑复制槽--')
        create_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"pg_recvlogical -d postgres " \
                     f"-U {self.primary_node.ssh_user} " \
                     f"-S slot_test003 " \
                     f"-p {self.primary_node.db_port} " \
                     f"-P mppdb_decoding --create"
        self.log.info(create_cmd)
        exec_msg = self.primary_node.sh(create_cmd).result()
        self.log.info(exec_msg)
        self.assertIn('FATAL', exec_msg)

    def tearDown(self):
        self.log.info('--步骤4:清理环境--')
        restore_cmd = Primary_SH.execute_gsguc('set',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               'wal_level=hot_standby')
        self.log.info(restore_cmd)
        restore_cmd = Primary_SH.execute_gsguc('set',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               'enable_slot_log=off')
        self.log.info(restore_cmd)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(
            '-Opengauss_Function_Standby_Logical_Replication_Case0003finish--')
