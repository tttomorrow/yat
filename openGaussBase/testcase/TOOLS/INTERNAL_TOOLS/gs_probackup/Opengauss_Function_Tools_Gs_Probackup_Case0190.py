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
Case Type   : 系统工具gs_probackup
Case Name   : 备机执行全量以及增量备份
Description :
    1.在postgresql.conf文件中添加参数enable_cbm_tracking=on并重启数据库
    2.进行初始化
    3.添加实例
    4.全量备机备份
    5.备机增量备份
    6.清理环境
Expect      :
    1.设置参数成功
    2.初始化成功
    3.添加实例成功
    4.全量备机备份成功
    5.备机增量备份成功
    6.清理环境成功
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

LOG = Logger()


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '需主备环境，若为单机环境则不执行')
class Probackup(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Standby1_User_Node = Node('Standby1DbUser')
        self.standby_sh = CommonSH('Standby1DbUser')
        self.constant = Constant()
        self.gs_probackup_bak_path = os.path.join(macro.DB_INSTANCE_PATH,
                                                  'test_slave_backup')
        LOG.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0190 start----')

    def test_server_tools(self):
        LOG.info('--步骤1:设置相关参数---')
        set_cmd = f"sed -i '$a\\enable_cbm_tracking=on' " \
                  f"{macro.DB_INSTANCE_PATH}/postgresql.conf"
        LOG.info(set_cmd)
        msg = self.Primary_User_Node.sh(set_cmd).result()
        LOG.info(msg)
        LOG.info('---步骤2:重启数据库---')
        restart_msg = Primary_SH.restart_db_cluster()
        LOG.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('---步骤3:查看设置参数是否生效---')
        msg = self.standby_sh.execut_db_sql('show enable_cbm_tracking;')
        LOG.info(msg)
        self.assertIn('on', msg)
        LOG.info('---步骤4:进行初始化---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup init -B {self.gs_probackup_bak_path};"
        LOG.info(init_cmd)
        init_msg = self.Standby1_User_Node.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg)
        LOG.info('---步骤5:添加实例---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup add-instance " \
                   f"-B {self.gs_probackup_bak_path}" \
                   f" --instance=test_slave_backup01 " \
                   f"-D {macro.DB_INSTANCE_PATH}"
        LOG.info(init_cmd)
        init_msg = self.Standby1_User_Node.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn("'test_slave_backup01' " + self.constant.init_success,
                      init_msg)
        LOG.info('---步骤6:全量备机备份---')
        probackup_cmd = f"source {macro.DB_ENV_PATH};" \
                        f"gs_probackup backup " \
                        f"-B {self.gs_probackup_bak_path} " \
                        f"-b FULL " \
                        f"--instance=test_slave_backup01 " \
                        f"-p {self.Standby1_User_Node.db_port} " \
                        f"-d postgres"
        LOG.info(probackup_cmd)
        init_msg = self.Standby1_User_Node.sh(probackup_cmd).result()
        LOG.info(init_msg)
        self.assertIn('completed', init_msg)
        LOG.info('---步骤7:增量备机备份---')
        probackup_cmd = f"source {macro.DB_ENV_PATH};" \
                        f"gs_probackup backup " \
                        f"-B {self.gs_probackup_bak_path} " \
                        f"-b PTRACK " \
                        f"--instance=test_slave_backup01 " \
                        f"-p {self.Standby1_User_Node.db_port} " \
                        f"-d postgres"
        LOG.info(probackup_cmd)
        init_msg = self.Standby1_User_Node.sh(probackup_cmd).result()
        LOG.info(init_msg)
        self.assertIn('completed', init_msg)
        LOG.info('---步骤8:查询---')
        query_cmd = f"source {macro.DB_ENV_PATH};" \
                    f"gs_probackup show -B {self.gs_probackup_bak_path}"
        LOG.info(query_cmd)
        excute_cmd = self.Standby1_User_Node.sh(query_cmd).result()
        LOG.info(excute_cmd)
        self.assertIn('OK', excute_cmd)

    def tearDown(self):
        LOG.info('---步骤8:清理环境---')
        clear_cmd = f'rm -rf {self.gs_probackup_bak_path}'
        LOG.info(clear_cmd)
        clear_msg = self.Standby1_User_Node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        cmd = f"sed -i '$d' {macro.DB_INSTANCE_PATH}/postgresql.conf;"
        LOG.info(cmd)
        msg = self.Primary_User_Node.sh(cmd).result()
        LOG.info(msg)
        restart_msg = Primary_SH.restart_db_cluster()
        LOG.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        LOG.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0190 end----')
