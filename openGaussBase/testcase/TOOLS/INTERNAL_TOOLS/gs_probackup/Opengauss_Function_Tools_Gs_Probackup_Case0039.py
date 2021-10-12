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
Case Type   : 系统内部使用工具
Case Name   : 指定-j，--skip-block-validation,--no-validate
              全量创建指定实例的备份
Description :
    1.设置参数enable_cbm_tracking=on
    2.新建目录
    3.进行初始化
    4.在备份路径内初始化一个新的备份实例
    5.执行全量备份
    6.删除新建目录，恢复参数文件
Expect      :
    1.参数设置成功
    2.新建目录成功
    3.进行初始化成功
    4.在备份路径内初始化一个新的备份实例成功
    5.执行全量备份
    6.删除新建目录成功，恢复参数文件成功
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup--------------------')
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0039开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('----------step1 设置相关参数---------------------')
        cmd1 = f"sed -i '$a\\enable_cbm_tracking=on' " \
            f"{macro.DB_INSTANCE_PATH}/postgresql.conf"
        LOG.info(cmd1)
        msg1 = self.PrimaryNode.sh(cmd1).result()
        LOG.info(msg1)
        LOG.info('---------step1.1 重启数据库-----------------------')
        self.sh_primary.restart_db_cluster()
        status = self.sh_primary.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)
        LOG.info('---------step1.2 查看设置参数是否生效--------------')
        msg = self.sh_primary.execut_db_sql('show enable_cbm_tracking;')
        LOG.info(msg)
        value = msg.splitlines()[-2].strip()
        self.assertIn('on', value)

        LOG.info('---------step2 新建备份目录--------------')
        init_cmd = f"mkdir {macro.DB_BACKUP_PATH}/testdir;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], init_msg)

        LOG.info('----------step3 进行初始化------------------')
        init_cmd = f"source {macro.DB_ENV_PATH};gs_probackup init -B " \
            f"{macro.DB_BACKUP_PATH}/testdir;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg)

        LOG.info('-----step4 在备份路径内初始化一个新的备份实例---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup add-instance -B {macro.DB_BACKUP_PATH}/testdir " \
            f"-D {macro.DB_INSTANCE_PATH} --instance=pro1;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn("'pro1' " + self.constant.init_success, init_msg)

        LOG.info('--------step5 执行增量备份-----------------------')
        back_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup -B {macro.DB_BACKUP_PATH}/testdir " \
            f" --instance=pro1 -b ptrack -d {self.PrimaryNode.db_name} -p " \
            f"{self.PrimaryNode.db_port} ; "
        LOG.info(back_cmd)
        back_msg = self.PrimaryNode.sh(back_cmd).result()
        LOG.info(back_msg)
        self.assertIn('Create new full backup before an incremental one',
                      back_msg)

    def tearDown(self):
        LOG.info('------------------this is tearDown--------------------')
        LOG.info('---------------step6 删除新建目录-----------------')
        clear_cmd = f"rm -rf {macro.DB_BACKUP_PATH}/testdir;"
        LOG.info(clear_cmd)
        clear_msg = self.PrimaryNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        cmd1 = f"sed -i '$d' {macro.DB_INSTANCE_PATH}/postgresql.conf;"
        LOG.info(cmd1)
        msg1 = self.PrimaryNode.sh(cmd1).result()
        LOG.info(msg1)
        LOG.info('---------step6.1 重启数据库-----------------------')
        self.sh_primary.restart_db_cluster()
        status = self.sh_primary.get_db_cluster_status()
        LOG.info(status)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0039执行完成-')
