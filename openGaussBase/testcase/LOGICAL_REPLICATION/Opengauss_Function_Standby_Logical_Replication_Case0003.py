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
Case Type   : 逻辑复制
Case Name   : 用户没有replication权限，主机创建逻辑复制槽，合理报错
Description :
        1.修改参数wal_level为logical;enable_slot_log为on
        2.主机创建逻辑复制槽
        3.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.合理报错
        3.清理环境完成
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '--Opengauss_Function_Standby_Logical_Replication_Case0003start-')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)
        self.slot_name = "slot_logical_replication_case0003"

    def test_standby_logical(self):
        text = '--step1:修改wal_level为logical;enable_slot_log为on;' \
               'expect:修改成功--'
        self.log.info(text)
        mod_msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'wal_level =logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'enable_slot_log =on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step2:主机创建逻辑复制槽;expect:报错--'
        self.log.info(text)
        create_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"pg_recvlogical -d postgres " \
                     f"-U {self.primary_node.ssh_user} " \
                     f"-S {self.slot_name} " \
                     f"-p {self.primary_node.db_port} " \
                     f"-P mppdb_decoding --create"
        self.log.info(create_cmd)
        exec_msg = self.primary_node.sh(create_cmd).result()
        self.log.info(exec_msg)
        self.assertIn('FATAL', exec_msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step3:清理环境;expect:清理环境完成--'
        self.log.info(text)
        res_cmd = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'wal_level=hot_standby')
        self.log.info(res_cmd)
        res_cmd = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'enable_slot_log=off')
        self.log.info(res_cmd)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Standby_Logical_Replication_Case0003finish--')
