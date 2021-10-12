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
Case Name   : 使用help显示gs_probackup add-instance命令的摘要信息
Description :
    1.执行命令显示gs_probackup add-instance命令的摘要信息
Expect      :
    1.显示gs_probackup add-instance命令的摘要信息成功
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
        LOG.info('--Opengauss_Function_Tools_Gs_Probackup_Case0128开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.except_msg = ['gs_probackup add-instance -B backup-path '
                           '-D pgdata-path --instance=instance_name',
                           '[-E external-directories-paths]',
                           '[--remote-proto=protocol] '
                           '[--remote-host=destination]',
                           '[--remote-path=path] [--remote-user=username]',
                           '[--remote-port=port] [--ssh-options=ssh_options]',
                           '-B, --backup-path=backup-path    '
                           'location of the backup storage area',
                           '-D, --pgdata=pgdata-path         '
                           'location of the database storage area',
                           '--instance=instance_name     '
                           'name of the new instance',
                           '-E, --external-dirs=external-directories-paths',
                           'backup some directories not from pgdata',
                           '(example: --external-dirs=/tmp/dir1:/tmp/dir2)',
                           '', 'Remote options:',
                           '--remote-proto=protocol      '
                           'remote protocol to use',
                           "available options: 'ssh', 'none' (default: ssh)",
                           '--remote-host=destination    '
                           'remote host address or hostname',
                           '--remote-port=port           '
                           'remote host port (default: 22)',
                           '--remote-path=path           path to directory '
                           'with gs_probackup binary on remote host',
                           '(default: current binary path)',
                           '--remote-user=username       user name for '
                           'ssh connection (default: current user)',
                           '--ssh-options=ssh_options    '
                           'additional ssh options (default: none)',
                           "(example: --ssh-options='-c cipher_"
                           "spec -F configfile')"]

    def test_system_internal_tools(self):
        LOG.info('------------------显示帮助信息------------------')
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
        gs_probackup help add-instance;
        '''
        LOG.info(check_cmd1)
        help_msg = self.PrimaryNode.sh(check_cmd1).result()
        LOG.info(help_msg)
        line_msg = help_msg.splitlines()
        LOG.info(line_msg)
        for j in line_msg:
            LOG.info(j)
            self.assertIn(j.strip(), self.except_msg)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        # 无须清理环境
        LOG.info(
            '---Opengauss_Function_Tools_Gs_Probackup_Case0128执行完成---')
