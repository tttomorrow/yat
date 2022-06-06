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
Case Name   : 执行set-config命令向pg_probackup.conf配置文件中添加设置信息
Description :
    1.新建目录
    2.进行初始化
    3.在备份路径内初始化一个新的备份实例
    4.向pg_probackup.conf配置文件中添加设置信息
    5.查看pg_probackup.conf配置文件中是否有添加信息
    6.删除新建目录
Expect      :
    1.新建目录成功
    2.进行初始化成功
    3.在备份路径内初始化一个新的备份实例成功
    4.向pg_probackup.conf配置文件中添加设置信息成功
    5.查看pg_probackup.conf配置文件，里面包含执行的添加信息
    6.删除新建目录成功
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
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0018开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('---------step1 新建备份目录--------------')
        init_cmd = f"mkdir {macro.DB_BACKUP_PATH}/testdir;" \
            f"mkdir {macro.DB_BACKUP_PATH}/dir1;" \
            f"mkdir {macro.DB_BACKUP_PATH}/dir2;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], init_msg)

        LOG.info('----------step2 进行初始化------------------')
        init_cmd = f"source {macro.DB_ENV_PATH};gs_probackup init -B " \
            f"{macro.DB_BACKUP_PATH}/testdir;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg)

        LOG.info('-----step3 在备份路径内初始化一个新的备份实例---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup add-instance -B {macro.DB_BACKUP_PATH}/testdir " \
            f"-D {macro.DB_INSTANCE_PATH} --instance=pro1;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn("'pro1' " + self.constant.init_success, init_msg)

        LOG.info('-----step4 向pg_probackup.conf配置文件中添加设置信息----')
        add_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup set-config -B {macro.DB_BACKUP_PATH}/testdir " \
            f" --instance=pro1 --pgdata={macro.DB_INSTANCE_PATH} " \
            f"--retention-redundancy=2 --retention-window=1 " \
            f"--compress-algorithm=none --compress-level=0 -d postgres  -p" \
            f"{self.PrimaryNode.db_port} -U {self.PrimaryNode.ssh_user} " \
            f"--external-dirs={macro.DB_BACKUP_PATH}/dir1 ;"
        LOG.info(add_cmd)
        add_msg = self.PrimaryNode.sh(add_cmd).result()
        LOG.info(add_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], add_msg)

        LOG.info('---step5 查看pg_probackup.conf配置文件中是否有添加信息---')
        cat_cmd = f"cat " \
            f"{macro.DB_BACKUP_PATH}/testdir/backups/pro1/pg_probackup.conf"
        LOG.info(cat_cmd)
        cat_msg = self.PrimaryNode.sh(cat_cmd).result()
        LOG.info(cat_msg)
        self.assertTrue(f'pgdata = {macro.DB_INSTANCE_PATH}' in cat_msg and
                        f'external-dirs = {macro.DB_BACKUP_PATH}/dir1' in
                        cat_msg and
                        'retention-redundancy = 2' in cat_msg and
                        'retention-window = 1' in cat_msg and
                        'compress-algorithm = none' in cat_msg and
                        'compress-level = 0' in cat_msg)

    def tearDown(self):
        LOG.info('------------------this is tearDown--------------------')
        LOG.info('---------------step6 删除新建目录-----------------')
        clear_cmd = f"rm -rf {macro.DB_BACKUP_PATH}/testdir;" \
            f"rm -rf {macro.DB_BACKUP_PATH}/dir1;" \
            f"rm -rf {macro.DB_BACKUP_PATH}/dir2;"
        LOG.info(clear_cmd)
        clear_msg = self.PrimaryNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0018执行完成-')
