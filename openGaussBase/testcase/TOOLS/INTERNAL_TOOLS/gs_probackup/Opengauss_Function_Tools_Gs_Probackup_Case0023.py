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
Case Type   : 系统内部使用工具
Case Name   : 只指定-B、--instance、--backup-id选项，
              执行gs_probackup set-backup
Description :
    1.新建目录
    2.进行初始化
    3.在备份路径内初始化一个新的备份实例
    4.向pg_probackup.conf配置文件中添加设置信息
    5.执行全量备份
    6.查看备份的外部文件
    7.只指定-B、--instance、--backup-id选项执行set-backup
    8.删除新建目录
Expect      :
    1.新建目录成功
    2.进行初始化成功
    3.在备份路径内初始化一个新的备份实例成功
    4.向pg_probackup.conf配置文件中添加设置信息成功
    5.执行全量备份成功
    6.查看备份的外部文件，该文件备份成功
    7.只指定-B、--instance、--backup-id选项执行set-backup失败
    8.删除新建目录成功
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup--------------------')
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0023开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('---------step1 新建备份目录--------------')
        instance_path = f'{macro.DB_INSTANCE_PATH}'
        LOG.info('实例路径为：' + instance_path)
        index1 = instance_path.find('/')
        index2 = instance_path.rfind('/')
        self.cluster_path = instance_path[index1:index2]
        LOG.info(self.cluster_path)
        init_cmd = f"mkdir {self.cluster_path}/testdir;" \
            f"mkdir {self.cluster_path}/testdir1;" \
            f"touch {self.cluster_path}/testdir1/probackup.sql;" \
            f"echo 'create table a(i int);' >> " \
            f"{self.cluster_path}/testdir1/probackup.sql;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], init_msg)

        LOG.info('----------step2 进行初始化------------------')
        init_cmd = f"source {macro.DB_ENV_PATH};gs_probackup init -B " \
            f"{self.cluster_path}/testdir;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg)

        LOG.info('-----step3 在备份路径内初始化一个新的备份实例---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup add-instance -B {self.cluster_path}/testdir " \
            f"-D {macro.DB_INSTANCE_PATH} --instance=pro1;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn("'pro1' " + self.constant.init_success, init_msg)

        LOG.info('-----step4 向pg_probackup.conf配置文件中添加设置信息----')
        add_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup set-config -B {self.cluster_path}/testdir " \
            f" --instance=pro1 --pgdata={macro.DB_INSTANCE_PATH}; "
        LOG.info(add_cmd)
        add_msg = self.PrimaryNode.sh(add_cmd).result()
        LOG.info(add_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], add_msg)

        LOG.info('--------------------step5 进行备份-------------------')
        back_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup -B {self.cluster_path}/testdir " \
            f" --instance=pro1 -b Full  -d {self.PrimaryNode.db_name} -p " \
            f"{self.PrimaryNode.db_port} " \
            f"--external-dirs={self.cluster_path}/testdir1; "
        LOG.info(back_cmd)
        back_msg = self.PrimaryNode.sh(back_cmd).result()
        LOG.info(back_msg)
        self.assertIn('completed', back_msg)
        self.backupmsg = back_msg.splitlines()[-1]
        LOG.info(self.backupmsg)
        self.backupid = self.backupmsg.split()[2]
        LOG.info('备份ID为：' + self.backupid)

        LOG.info('--------------step6 查看备份的外部文件---------------')
        backup_cmd = f"ls {self.cluster_path}/testdir/backups/pro1/" \
            f"{self.backupid}/external_directories/externaldir1"
        LOG.info(backup_cmd)
        backup_msg = self.PrimaryNode.sh(backup_cmd).result()
        LOG.info(backup_msg)
        self.assertIn('probackup.sql', backup_msg)

        LOG.info('--------------step7 执行set-backup---------------')
        backup_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup set-backup -B {self.cluster_path}/testdir " \
            f" --instance=pro1 --backup-id {self.backupid}; "
        LOG.info(backup_cmd)
        backup_msg = self.PrimaryNode.sh(backup_cmd).result()
        LOG.info(backup_msg)
        self.assertIn("Nothing to set by 'set-backup' command", backup_msg)

    def tearDown(self):
        LOG.info('------------------this is tearDown--------------------')
        LOG.info('---------------step8 删除新建目录-----------------')
        clear_cmd = f"rm -rf {self.cluster_path}/testdir;" \
            f"rm -rf {self.cluster_path}/testdir1;"
        LOG.info(clear_cmd)
        clear_msg = self.PrimaryNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0023执行完成-')
