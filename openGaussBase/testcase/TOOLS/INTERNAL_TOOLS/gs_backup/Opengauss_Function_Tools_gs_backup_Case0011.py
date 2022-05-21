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
Case Name   : 关闭备数据库，指定参数--all执行gs_backup进行备份，是否会
                备份参数文件与二进制文件
Description :
    1.创建备份目录
    2.关闭数据库备机
    3.指定参数--all执行gs_backup
    4.查看主机与备机对应目录，该目录是否存放参数文件与二进制文件
    5.开启备机
Expect      :
    1.创建备份目录成功
    2.关闭备机成功
    3.指定参数--all执行gs_backup成功
    4.查看主机与备机对应目录成功，该目录存放参数文件与二进制文件
    5.开启备机成功
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
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0011开始执行---')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('----------若为单机环境，后续不执行，直接通过-----------')
        query_cmd = f''' source {macro.DB_ENV_PATH}
            gs_om -t status --detail
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        if 'Standby' not in query_msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.StandbyNode = Node('Standby1DbUser')
            self.sh_standby = CommonSH('Standby1DbUser')

            LOG.info('-----------------新建备份目录-----------------')
            mkdir_cmd = f"mkdir {macro.DB_BACKUP_PATH}/tesdir;"
            LOG.info(mkdir_cmd)
            mkdir_msg = self.StandbyNode.sh(mkdir_cmd).result()
            LOG.info(mkdir_msg)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], mkdir_msg)

            LOG.info('-------------------关闭备机--------------------')
            stop_msg = self.sh_standby.stop_db_instance()
            self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG, stop_msg)

            LOG.info('--------------执行gs_backup进行备份-----------')
            backup_cmd = f'''source {macro.DB_ENV_PATH};
                gs_backup -t backup \
                --backup-dir={macro.DB_BACKUP_PATH}/tesdir --all;
                '''
            LOG.info(backup_cmd)
            backup_msg = self.StandbyNode.sh(backup_cmd).result()
            LOG.info(backup_msg)
            self.assertIn(self.constant.gs_backup_success, backup_msg)

            LOG.info('--------------查看主机备份文件-----------')
            ls_cmd = f'ls {macro.DB_BACKUP_PATH}/tesdir;'
            LOG.info(ls_cmd)
            ls_msg = self.PrimaryNode.sh(ls_cmd).result()
            LOG.info(ls_msg)
            self.assertIn('parameter.tar', ls_msg)
            self.assertIn('binary.tar', ls_msg)

            LOG.info('--------------查看备机备份文件-----------')
            ls_cmd = f'ls {macro.DB_BACKUP_PATH}/tesdir;'
            LOG.info(ls_cmd)
            ls_msg = self.StandbyNode.sh(ls_cmd).result()
            LOG.info(ls_msg)
            self.assertIn('parameter.tar', ls_msg)
            self.assertIn('binary.tar', ls_msg)

    def tearDown(self):
        LOG.info('-----------------this is tearDown-------------------')
        start_cmd = f''' source {macro.DB_ENV_PATH};
            gs_om -t start;
            '''
        LOG.info(start_cmd)
        start_msg = self.PrimaryNode.sh(start_cmd).result()
        LOG.info(start_msg)
        query_cmd = f''' source {macro.DB_ENV_PATH}
            gs_om -t status --detail
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        if 'Standby' not in query_msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.StandbyNode = Node('Standby1DbUser')
            clear_cmd1 = f"rm -rf {macro.DB_BACKUP_PATH}/tesdir"
            LOG.info(clear_cmd1)
            clear_msg1 = self.PrimaryNode.sh(clear_cmd1).result()
            LOG.info(clear_msg1)
            clear_cmd2 = f"rm -rf {macro.DB_BACKUP_PATH}/tesdir"
            LOG.info(clear_cmd2)
            clear_msg2 = self.StandbyNode.sh(clear_cmd2).result()
            LOG.info(clear_msg2)
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0011执行完成---')
