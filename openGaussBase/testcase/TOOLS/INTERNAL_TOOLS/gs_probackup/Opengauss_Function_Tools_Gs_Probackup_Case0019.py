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
Case Name   : 执行set-config命令修改pg_probackup.conf配置文件中
              已添加的设置信息
Description :
    1.新建目录
    2.进行初始化
    3.在备份路径内初始化一个新的备份实例
    4.向pg_probackup.conf配置文件中添加设置信息
    5.查看pg_probackup.conf配置文件中是否有添加信息
    6.修改pg_probackup.conf配置文件中实例目录信息
    7.查看pg_probackup.conf配置文件中信息是否已修改
    8.删除新建目录
Expect      :
    1.新建目录成功
    2.进行初始化成功
    3.在备份路径内初始化一个新的备份实例成功
    4.向pg_probackup.conf配置文件中添加设置信息成功
    5.查看pg_probackup.conf配置文件，里面包含执行的添加信息
    6.修改pg_probackup.conf配置文件中实例目录信息成功
    7.查看pg_probackup.conf配置文件中信息，实例目录信息已修改
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
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0019开始执行-')
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
            f" --instance=pro1 --pgdata={macro.DB_INSTANCE_PATH}; "
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
        self.assertIn(f'pgdata = {macro.DB_INSTANCE_PATH}', cat_msg)

        LOG.info('-----step6 修改pg_probackup.conf配置文件中实例目录信息---')
        alter_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup set-config -B {macro.DB_BACKUP_PATH}/testdir " \
            f" --instance=pro1 --pgdata={macro.DB_INSTANCE_PATH}/alterdir;"
        LOG.info(alter_cmd)
        alter_msg = self.PrimaryNode.sh(alter_cmd).result()
        LOG.info(alter_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], alter_msg)

        LOG.info('---step7 查看pg_probackup.conf配置文件中是否已修改---')
        cat_cmd = f"cat " \
            f"{macro.DB_BACKUP_PATH}/testdir/backups/pro1/pg_probackup.conf"
        LOG.info(cat_cmd)
        cat_msg = self.PrimaryNode.sh(cat_cmd).result()
        LOG.info(cat_msg)
        self.assertIn(f'pgdata = {macro.DB_INSTANCE_PATH}/alterdir', cat_msg)

    def tearDown(self):
        LOG.info('------------------this is tearDown--------------------')
        LOG.info('---------------step6 删除新建目录-----------------')
        clear_cmd = f"rm -rf {macro.DB_BACKUP_PATH}/testdir;" \
            f"rm -rf {macro.DB_BACKUP_PATH}/dir1;" \
            f"rm -rf {macro.DB_BACKUP_PATH}/dir2;"
        LOG.info(clear_cmd)
        clear_msg = self.PrimaryNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0019执行完成-')
