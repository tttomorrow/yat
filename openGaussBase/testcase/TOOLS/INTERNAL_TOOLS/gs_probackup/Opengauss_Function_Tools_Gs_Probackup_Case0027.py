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
Case Name   : 查看gs_probackup backup命令的摘要信息
Description :
    1.执行命令显示gs_probackup backup命令的摘要信息
Expect      :
    1.显示gs_probackup backup命令的摘要信息成功
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
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0027开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.except_msg = ['gs_probackup backup -B backup-path '
                           '--instance=instance_name -b backup-mode',
                           '[-D pgdata-path] [-C] [-S slot-name] '
                           '[--temp-slot]',
                           '[--backup-pg-log] [-j threads_num] [--progress]',
                           '[--no-validate] [--skip-block-validation]',
                           '[-E external-directories-paths]',
                           '[--no-sync] [--note=text]',
                           '[--archive-timeout=timeout]',
                           '[--log-level-console=log-level-console]',
                           '[--log-level-file=log-level-file]',
                           '[--log-filename=log-filename]',
                           '[--error-log-filename=error-log-filename]',
                           '[--log-directory=log-directory]',
                           '[--log-rotation-size=log-rotation-size]',
                           '[--log-rotation-age=log-rotation-age]',
                           '[--delete-expired] [--delete-wal] '
                           '[--merge-expired]',
                           '[--retention-redundancy=retention-redundancy]',
                           '[--retention-window=retention-window]',
                           '[--wal-depth=wal-depth] [--dry-run]',
                           '[--compress-algorithm=compress-algorithm]',
                           '[--compress-level=compress-level]',
                           '[--compress]',
                           '[-d dbname] [-h host] [-p port] [-U username]'
                           ' [-w] [-W password]',
                           '[-t rw-timeout]',
                           '[--remote-proto=protocol] '
                           '[--remote-host=destination]',
                           '[--remote-path=path] [--remote-user=username]',
                           '[--remote-port=port] [--ssh-options=ssh_options]',
                           '[--ttl=interval] [--expire-time=time]', '',
                           '-B, --backup-path=backup-path    '
                           'location of the backup storage area',
                           '--instance=instance_name     '
                           'name of the instance',
                           '-b, --backup-mode=backup-mode    '
                           'backup mode=FULL|PTRACK',
                           '-D, --pgdata=pgdata-path         '
                           'location of the database storage area',
                           '-C, --smooth-checkpoint          '
                           'do smooth checkpoint before backup',
                           '-S, --slot=slot-name             '
                           'replication slot to use',
                           '--temp-slot                  '
                           'use temporary replication slot',
                           "--backup-pg-log              "
                           "backup of 'pg_log' directory",
                           '-j, --threads=threads_num        '
                           'number of parallel threads',
                           '-t, --rw-timeout=rw-timeout      '
                           'read-write timeout during idle connection',
                           '--progress                   show progress',
                           '--no-validate                '
                           'disable validation after backup',
                           '--skip-block-validation      '
                           'set to validate only file-level checksum',
                           '-E, --external-dirs=external-directories-paths',
                           'backup some directories not from pgdata',
                           '(example: --external-dirs=/tmp/dir1:/tmp/dir2)',
                           '--no-sync                    '
                           'do not sync backed up files to disk',
                           '--note=text                  add note to backup',
                           "(example: --note='backup before "
                           "app update to v13.1')",
                           '--archive-timeout=timeout    wait timeout for '
                           'WAL segment archiving (default: 5min)',
                           '', 'Logging options:',
                           '--log-level-console=log-level-console',
                           'level for console logging (default: info)',
                           "available options: 'off', 'error', 'warning', "
                           "'info', 'log', 'verbose'",
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
                           "(default: min)",
                           '',
                           'Retention options:',
                           '--delete-expired             '
                           'delete backups expired according to current',
                           'retention policy after '
                           'successful backup completion',
                           '--merge-expired              '
                           'merge backups expired according to current',
                           'retention policy after successful '
                           'backup completion',
                           '--delete-wal                 '
                           'remove redundant files in WAL archive',
                           '--retention-redundancy=retention-redundancy',
                           'number of full backups to keep; '
                           '0 disables; (default: 0)',
                           '--retention-window=retention-window',
                           'number of days of recoverability; '
                           '0 disables; (default: 0)',
                           '--wal-depth=wal-depth        number of latest '
                           'valid backups per timeline that must',
                           'retain the ability to perform PITR; 0 disables; '
                           '(default: 0)',
                           '--dry-run                    '
                           'perform a trial run without any changes',
                           '', 'Compression options:',
                           '--compress-algorithm=compress-algorithm',
                           "available options: 'zlib', 'pglz', 'none'"
                           " (default: none)",
                           '--compress-level=compress-level',
                           'level of compression [0-9] (default: 1)',
                           "--compress                   alias for "
                           "--compress-algorithm='zlib' and "
                           "--compress-level=1",
                           '', 'Connection options:',
                           '-U, --pguser=username            '
                           'user name to connect as '
                           '(default: current local user)',
                           '-d, --pgdatabase=dbname          '
                           'database to connect (default: username)',
                           "-h, --pghost=hostname            database server "
                           "host or socket directory(default: 'local socket')",
                           '-p, --pgport=port                '
                           'database server port (default: 5432)',
                           '-w, --no-password                '
                           'never prompt for password',
                           '-W, --password=password          '
                           'the password of specified database user',
                           '', 'Remote options:',
                           '--remote-proto=protocol      '
                           'remote protocol to use',
                           "available options: 'ssh', 'none' (default: ssh)",
                           '--remote-host=destination    '
                           'remote host address or hostname',
                           '--remote-port=port           '
                           'remote host port (default: 22)',
                           '--remote-path=path           path to directory'
                           ' with gs_probackup binary on remote host',
                           '(default: current binary path)',
                           '--remote-user=username       user name for ssh '
                           'connection (default: current user)',
                           '--ssh-options=ssh_options    additional ssh '
                           'options (default: none)',
                           "(example: --ssh-options='-c cipher_spec "
                           "-F configfile')",
                           '',
                           'Pinning options:',
                           '--ttl=interval               pin backup for '
                           'specified amount of time; 0 unpin',
                           "available units: 'ms', 's', 'min', 'h', "
                           "'d' (default: s)",
                           '(example: --ttl=20d)',
                           '--expire-time=time           '
                           'pin backup until specified time stamp',
                           "(example: --expire-time="
                           "'2024-01-01 00:00:00+03')"]

    def test_system_internal_tools(self):
        LOG.info('step1 执行命令显示gs_probackup backup命令的摘要信息')
        help_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup --help;"
        LOG.info(help_cmd)
        help_msg = self.PrimaryNode.sh(help_cmd).result()
        LOG.info(help_msg)
        temp = help_msg.splitlines()
        options_list = []
        for j in temp:
            options_list.append(j.strip())
        LOG.info(options_list)
        self.assertEqual(options_list, self.except_msg)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        # 无须清理环境
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0027执行完成-')
