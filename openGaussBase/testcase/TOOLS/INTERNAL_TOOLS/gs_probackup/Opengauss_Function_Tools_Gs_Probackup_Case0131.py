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
Case Name   : 使用help显示gs_probackup set-backup命令的摘要信息
Description :
    1.执行命令显示gs_probackup set-backup命令的摘要信息
Expect      :
    1.显示gs_probackup set-backup命令的摘要信息成功
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
        LOG.info('--Opengauss_Function_Tools_Gs_Probackup_Case0131开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.except_msg = ['gs_probackup set-backup -B backup-path '
                           '--instance=instance_name -i backup-id',
                           '[--note=text] [--ttl=interval] '
                           '[--expire-time=time]',
                           '',
                           '-B, --backup-path=backup-path    '
                           'location of the backup storage area',
                           '--instance=instance_name     '
                           'name of the instance',
                           '-i, --backup-id=backup-id        backup id',
                           "--note=text                  add note to "
                           "backup; 'none' to remove note",
                           "(example: --note='backup before app "
                           "update to v13.1')",
                           '--ttl=interval               pin backup '
                           'for specified amount of time; 0 unpin',
                           "available units: 'ms', 's', 'min', 'h', "
                           "'d' (default: s)",
                           '(example: --ttl=20d)',
                           '--expire-time=time           pin backup '
                           'until specified time stamp',
                           "(example: --expire-time="
                           "'2024-01-01 00:00:00+03')"]

    def test_system_internal_tools(self):
        LOG.info('------------------显示帮助信息------------------')
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
        gs_probackup help set-backup;
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
            '---Opengauss_Function_Tools_Gs_Probackup_Case0131执行完成---')
