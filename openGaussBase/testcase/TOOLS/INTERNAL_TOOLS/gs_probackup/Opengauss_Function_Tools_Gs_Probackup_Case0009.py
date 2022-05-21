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
Case Name   : gs_probackup初始化备份路径已存在但无权限
Description :
    1.新建备份目录并去除权限
    2.使用gs_probackup对备份目录进行初始化
Expect      :
    1.新建备份目录并去除权限成功
    2.使用gs_probackup对备份目录进行初始化失败
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
        LOG.info('---Opengauss_Function_Tools_Gs_Probackup_Case0009开始执行---')
        self.constant = Constant()
        self.rootNode = Node('PrimaryRoot')
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        query_cmd = f''' source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        if 'Standby' not in query_msg:
            LOG.info('----------单机环境，后续不执行，直接通过----------')
        else:
            LOG.info('-----------新建目录--------------')
            init_cmd = f'''mkdir {macro.DB_BACKUP_PATH}/testzl;
                chmod 000 {macro.DB_BACKUP_PATH}/testzl'''
            LOG.info(init_cmd)
            init_msg = self.PrimaryNode.sh(init_cmd).result()
            LOG.info(init_msg)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], init_msg)

            LOG.info('------------------进行初始化------------------')
            init_cmd = f'''source {macro.DB_ENV_PATH};
                gs_probackup init -B {macro.DB_BACKUP_PATH}/testzl;
                '''
            LOG.info(init_cmd)
            init_msg = self.PrimaryNode.sh(init_cmd).result()
            LOG.info(init_msg)
            self.assertIn(self.constant.PERMISSION_DENY_MSG, init_msg)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        query_cmd = f''' source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        if 'Standby' not in query_msg:
            LOG.info('----------单机环境，后续不执行，直接通过----------')
        else:
            clear_cmd = f'rm -rf {macro.DB_BACKUP_PATH}/testzl'
            LOG.info(clear_cmd)
            clear_msg = self.rootNode.sh(clear_cmd).result()
            LOG.info(clear_msg)
        LOG.info('---Opengauss_Function_Tools_Gs_Probackup_Case0009执行完成---')
