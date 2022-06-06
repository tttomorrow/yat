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
Case Name   : 使用gs_probackup backup命令指定--compress-algorithm=zlib和 
              --compress-level=10，合理报错
Description :
    1.新建备份目录
    2.进行初始化
    3.在备份路径内初始化一个新的备份实例
    4.查看是否生成pg_probackup.conf配置文件
    5.创建指定实例的备份，添加压缩相关参数
    6.删除新建目录
Expect      :
    1.新建备份目录成功
    2.进行初始化成功
    3.初始化新的备份实例成功
    4.生成pg_probackup.conf配置文件，该文件保存了指定数据目录pgdata-path的
    gs_probackup设置
    5.备份失败
    6.删除新建目录成功
History     :
"""

import os
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('--Opengauss_Function_Tools_Gs_Probackup_Case0183start--')
        self.constant = Constant()
        self.Primary_Node = Node('PrimaryDbUser')
        self.gs_probackup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                                  'testdir183')

    def test_system_internal_tools(self):
        LOG.info('---step1新建备份目录---')
        mkdir_cmd = f'''if [ ! -d "{self.gs_probackup_bak_path}" ]
                                then
                                    mkdir -p {self.gs_probackup_bak_path}
                                fi'''
        LOG.info(mkdir_cmd)
        primary_result = self.Primary_Node.sh(mkdir_cmd).result()
        LOG.info(primary_result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], primary_result)
        LOG.info('---step2进行初始化---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup init -B {self.gs_probackup_bak_path};"
        LOG.info(init_cmd)
        init_msg = self.Primary_Node.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg)
        LOG.info('---step3在备份路径内初始化一个新的备份实例---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup add-instance " \
                   f"-B {self.gs_probackup_bak_path} " \
                   f"-D {macro.DB_INSTANCE_PATH} " \
                   f"--instance=test_183; "
        LOG.info(init_cmd)
        init_msg = self.Primary_Node.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn("'test_183' " + self.constant.init_success, init_msg)
        LOG.info('---step4查看pg_probackup.conf配置文件---')
        cat_cmd = f"cat {self.gs_probackup_bak_path}/backups/" \
                  f"test_183/pg_probackup.conf"
        LOG.info(cat_cmd)
        cat_msg = self.Primary_Node.sh(cat_cmd).result()
        LOG.info(cat_msg)
        self.assertIn(f'pgdata = {macro.DB_INSTANCE_PATH}', cat_msg)
        LOG.info('---step5创建指定实例的备份，添加压缩相关参数---')
        backup_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_probackup backup " \
                     f"-B {self.gs_probackup_bak_path} " \
                     f"--instance=test_183  " \
                     f"-b FULL  " \
                     f"--compress-algorithm=zlib " \
                     f"--compress-level=10 " \
                     f"-d postgres " \
                     f"-p {self.Primary_Node.db_port}"
        LOG.info(backup_cmd)
        exec_msg = self.Primary_Node.sh(backup_cmd).result()
        LOG.info(exec_msg)
        self.assertIn('ERROR: --compress-level value must be in the range '
                      'from 0 to 9', exec_msg)

    def tearDown(self):
        LOG.info('---step6删除新建目录---')
        clear_cmd = f'rm -rf {self.gs_probackup_bak_path}'
        LOG.info(clear_cmd)
        clear_msg = self.Primary_Node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0183finish-')
