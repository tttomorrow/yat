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
Case Type   : 数据库系统
Case Name   : gs_probackup 在备节点上增量备份
Description :
    1. 需在postgresql.conf中手动添加参数“enable_cbm_tracking = on”。
    2. 初始化备份目录（备节点）
    3. 添加备份实例（备节点）
    4. 全量备份（备节点）
    5. 增量备份（备节点）
Expect      :
    1.添加成功
    2.初始化成功
    3.添加成功
    4.全量备份成功
    5.增量备份成功
History     :
"""
import unittest
import os
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

primary_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 '需主备环境，若为单机环境则不执行')
class RecoveryDelay(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_Tools_Gs_Probackup_Case0189 start")
        self.constant = Constant()
        self.db_standby_user_node = Node(node='Standby1DbUser')
        self.commsh_sta = CommonSH('Standby1DbUser')
        self.parent_path = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.backup_path = os.path.join(self.parent_path, 'probackup')
        self.instance_name = 'probackup189'

    def test_index(self):

        self.log.info('--------1.enable_cbm_tracking = on-------')
        cmd = f"echo 'enable_cbm_tracking = on' >> " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, macro.DB_PG_CONFIG_NAME)}"
        self.log.info(cmd)
        self.db_standby_user_node.sh(cmd)
        result = self.commsh_sta.restart_db_cluster()
        self.assertTrue(result)

        self.log.info('--------2.初始化备份目录（备节点）-------')
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup init -B {self.backup_path}"
        self.log.info(cmd)
        result = self.db_standby_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('successfully inited', result)

        self.log.info('--------3添加备份实例（备节点）-------')
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup add-instance -B {self.backup_path} " \
            f"-D {macro.DB_INSTANCE_PATH} --instance {self.instance_name}"
        self.log.info(cmd)
        result = self.db_standby_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('successfully inited', result)

        self.log.info('--------4.全量备份（备节点）-------')
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup -B {self.backup_path} -b Full --stream " \
            f"--instance {self.instance_name} " \
            f"-U {self.db_standby_user_node.db_user} " \
            f"-d {self.db_standby_user_node.db_name} " \
            f"-p {self.db_standby_user_node.db_port} " \
            f"-W {self.db_standby_user_node.db_password}"
        self.log.info(cmd)
        result = self.db_standby_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('completed', result)
        self.assertIn('Wait a few minutes to get the target LSN or the last '
                      'valid record prior to the target LSN', result)

        self.log.info('--------5增量备份（备节点）-------')
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup -B {self.backup_path} -b PTRACK --stream " \
            f"--instance {self.instance_name} " \
            f"-U {self.db_standby_user_node.db_user} " \
            f"-d {self.db_standby_user_node.db_name} " \
            f"-p {self.db_standby_user_node.db_port} " \
            f"-W {self.db_standby_user_node.db_password}"
        self.log.info(cmd)
        result = self.db_standby_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('completed', result)
        self.assertIn('Wait a few minutes to get the target LSN or the last '
                      'valid record prior to the target LSN', result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('--------删除备份路径-------')
        cmd = f"rm -rf {self.backup_path}"
        self.log.info(cmd)
        result = self.db_standby_user_node.sh(cmd).result()
        self.log.info(result)

        self.log.info("--------------恢复配置文件----------------")
        cmd = f"sed -i '$d' " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, macro.DB_PG_CONFIG_NAME)}"
        self.log.info(cmd)
        result = self.db_standby_user_node.sh(cmd).result()
        self.log.info(result)
        result = self.commsh_sta.restart_db_cluster()
        self.log.info(result)
        self.log.info("Opengauss_Function_Tools_Gs_Probackup_Case0189 end")