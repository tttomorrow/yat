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
Case Name   : 使用help显示gs_probackup delete命令的摘要信息
Description :
    1.执行命令显示gs_probackup delete命令的摘要信息
Expect      :
    1.显示gs_probackup delete命令的摘要信息成功
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
        LOG.info('--Opengauss_Function_Tools_Gs_Probackup_Case0137开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.except_msg = ['gs_probackup delete -B backup-path '
                           '--instance=instance_name',
                           '[-i backup-id | --delete-expired | --merge-'
                           'expired | --status=backup_status]',
                           '[--delete-wal] [-j threads_num] [--progress]',
                           '[--retention-redundancy=retention-redundancy]',
                           '[--retention-window=retention-window]',
                           '[--wal-depth=wal-depth] [--dry-run]',
                           '[--log-level-console=log-level-console]',
                           '[--log-level-file=log-level-file]',
                           '[--log-filename=log-filename]',
                           '[--error-log-filename=error-log-filename]',
                           '[--log-directory=log-directory]',
                           '[--log-rotation-size=log-rotation-size]',
                           '[--log-rotation-age=log-rotation-age]',
                           '',
                           '-B, --backup-path=backup-path    '
                           'location of the backup storage area',
                           '--instance=instance_name     '
                           'name of the instance',
                           '-i, --backup-id=backup-id        '
                           'backup to delete',
                           '--status=backup_status       delete all backups '
                           'with specified status',
                           '-j, --threads=threads_num        '
                           'number of parallel threads',
                           '--progress                   show progress',
                           '',
                           'Retention options:',
                           '--delete-expired             delete backups '
                           'expired according to current',
                           'retention policy',
                           '--merge-expired              merge backups '
                           'expired according to current',
                           'retention policy',
                           '--delete-wal                 remove redundant '
                           'files in WAL archive',
                           '--retention-redundancy=retention-redundancy',
                           'number of full backups to keep; 0 disables; '
                           '(default: 0)',
                           '--retention-window=retention-window',
                           'number of days of recoverability; '
                           '0 disables; (default: 0)',
                           '--wal-depth=wal-depth        number of latest '
                           'valid backups per timeline that must',
                           'retain the ability to perform PITR; 0 disables; '
                           '(default: 0)',
                           '--dry-run                    '
                           'perform a trial run without any changes',
                           '', 'Logging options:',
                           '--log-level-console=log-level-console',
                           'level for console logging (default: info)',
                           "available options: 'off', 'error', 'warning',"
                           " 'info', 'log', 'verbose'",
                           '--log-level-file=log-level-file',
                           'level for file logging (default: off)',
                           "available options: 'off', 'error', 'warning', "
                           "'info', 'log', 'verbose'",
                           '--log-filename=log-filename',
                           "filename for file logging "
                           "(default: 'pg_probackup.log')",
                           'support strftime format (example: '
                           'pg_probackup-%Y-%m-%d_%H%M%S.log)',
                           '--error-log-filename=error-log-filename',
                           'filename for error logging (default: none)',
                           '--log-directory=log-directory',
                           'directory for file logging '
                           '(default: BACKUP_PATH/log)',
                           '--log-rotation-size=log-rotation-size',
                           'rotate logfile if its size exceeds this value; '
                           '0 disables; (default: 0)',
                           "available units: 'kB', 'MB', 'GB', 'TB' "
                           "(default: kB)",
                           '--log-rotation-age=log-rotation-age',
                           'rotate logfile if its age exceeds this value; '
                           '0 disables; (default: 0)',
                           "available units: 'ms', 's', 'min', 'h', 'd' "
                           "(default: min)"]

    def test_system_internal_tools(self):
        LOG.info('------------------显示帮助信息------------------')
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
        gs_probackup help delete;
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
        LOG.info('--Opengauss_Function_Tools_Gs_Probackup_Case0137执行完成--')
