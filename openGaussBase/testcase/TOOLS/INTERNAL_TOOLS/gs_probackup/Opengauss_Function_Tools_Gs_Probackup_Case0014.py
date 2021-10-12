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
Case Name   : 使用不正确的实例名在备份路径backup_dir内
              删除指定实例相关的备份内容
Description :
    1.新建目录
    2.进行初始化
    3.在备份路径内初始化一个新的备份实例
    4.在备份路径backup-path内删除指定实例相关的备份内容
    5.删除新建目录
Expect      :
    1.新建目录成功
    2.进行初始化成功
    3.在备份路径内初始化一个新的备份实例
    4.在备份路径backup-path内删除指定实例相关的备份内容失败，
    报错Instance 'pro2' does not exist in this backup catalog
    5.删除新建目录成功
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
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0014开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('---------step1 新建备份目录--------------')
        init_cmd = f"mkdir {macro.DB_BACKUP_PATH}/testdir;"
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

        LOG.info('-step4 在备份路径backup-path内删除指定实例相关的备份内容-')
        del_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup del-instance -B {macro.DB_BACKUP_PATH}/testdir " \
            f" --instance=pro2;"
        LOG.info(del_cmd)
        del_msg = self.PrimaryNode.sh(del_cmd).result()
        LOG.info(del_msg)
        self.assertIn(self.constant.NOT_EXIST, del_msg)

    def tearDown(self):
        LOG.info('------------------this is tearDown--------------------')
        LOG.info('---------------step5 删除新建目录-----------------')
        clear_cmd = f"rm -rf {macro.DB_BACKUP_PATH}/testdir;"
        LOG.info(clear_cmd)
        clear_msg = self.PrimaryNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0014执行完成-')
