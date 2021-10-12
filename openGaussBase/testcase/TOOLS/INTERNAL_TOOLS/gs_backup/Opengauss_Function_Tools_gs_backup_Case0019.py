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
Case Name   : 主备备份后使用系统用户执行gs_backup进行恢复（备份路径权限不足）
Description :
    1.新建备份目录
    2.执行gs_backup对参数文件进行备份
    3.去除备份文件目录的权限
    4.执行gs_backup对参数文件进行恢复
Expect      :
    1.切换用户成功
    2.执行gs_backup备份成功，提示信息为：Successfully backed up cluster files.
    3.去除备份文件目录的权限成功
    4.执行gs_backup对参数文件进行恢复
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
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0019开始执行---')
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
            LOG.info('-----------------新建备份目录-----------------')
            mkdir_cmd = f"mkdir {macro.DB_BACKUP_PATH}/tesdir;"
            LOG.info(mkdir_cmd)
            mkdir_msg = self.PrimaryNode.sh(mkdir_cmd).result()
            LOG.info(mkdir_msg)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], mkdir_msg)

            LOG.info('--------------执行gs_backup进行备份-----------')
            backup_cmd = f'''source {macro.DB_ENV_PATH};
                gs_backup -t backup \
                --backup-dir={macro.DB_BACKUP_PATH}/tesdir ;
                '''
            LOG.info(backup_cmd)
            backup_msg = self.PrimaryNode.sh(backup_cmd).result()
            LOG.info(backup_msg)
            self.assertIn(self.constant.gs_backup_success, backup_msg)

            LOG.info('-------------去除备份目录权限-----------------')
            chmod_cmd = f"chmod 000 {macro.DB_BACKUP_PATH}/tesdir;"
            LOG.info(chmod_cmd)
            chmod_msg = self.PrimaryNode.sh(chmod_cmd).result()
            LOG.info(chmod_msg)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], chmod_msg)

            LOG.info('--------------执行gs_backup进行还原-----------')
            backup_cmd = f'''source {macro.DB_ENV_PATH};
                gs_backup -t restore \
                --backup-dir={macro.DB_BACKUP_PATH}/tesdir ;
                '''
            LOG.info(backup_cmd)
            backup_msg = self.PrimaryNode.sh(backup_cmd).result()
            LOG.info(backup_msg)
            self.assertIn(self.constant.PERMISSION_DENY_MSG, backup_msg)

    def tearDown(self):
        LOG.info('-----------------this is tearDown-------------------')
        query_cmd = f''' source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        if 'Standby' not in query_msg:
            LOG.info('----------单机环境，后续不执行，直接通过----------')
        else:
            self.StandbyNode = Node('Standby1DbUser')
            clear_cmd = f"rm -rf {macro.DB_BACKUP_PATH}/tesdir"
            LOG.info(clear_cmd)
            clear_msg1 = self.rootNode.sh(clear_cmd).result()
            LOG.info(clear_msg1)
            clear_msg2 = self.StandbyNode.sh(clear_cmd).result()
            LOG.info(clear_msg2)
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0019执行完成---')
