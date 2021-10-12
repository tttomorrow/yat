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
Case Name   : 使用系统用户执行gs_backup进行恢复
Description :
    1.使用系统用户执行gs_backup进行恢复
Expect      :
    1.使用系统用户执行gs_backup进行恢复成功
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
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0018开始执行---')
        self.constant = Constant()
        self.rootNode = Node('PrimaryRoot')
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
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

            LOG.info('--------------执行gs_backup进行还原-----------')
            restore_cmd = f'''source {macro.DB_ENV_PATH};
                gs_backup -t restore \
                --backup-dir={macro.DB_BACKUP_PATH}/tesdir ;
                '''
            LOG.info(restore_cmd)
            restor_msg = self.PrimaryNode.sh(restore_cmd).result()
            LOG.info(restor_msg)
            self.assertIn(self.constant.gs_backup_restore_success, restor_msg)

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
            clear_msg1 = self.PrimaryNode.sh(clear_cmd).result()
            LOG.info(clear_msg1)
            clear_msg2 = self.StandbyNode.sh(clear_cmd).result()
            LOG.info(clear_msg2)
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0018执行完成---')
