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
Case Name   : 显示gs_probackup命令的摘要信息
Description :
    1.执行命令显示gs_probackup命令的摘要信息
Expect      :
    1.显示gs_probackup命令的摘要信息成功
History     :
"""

import unittest
import os
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.except_msg = ['gs_probackup - utility to manage backup/recovery'
                           ' of openGauss database.',
                           '', 'gs_probackup help [COMMAND]', '',
                           'gs_probackup version', '',
                           'gs_probackup init -B backup-path [--help]', '',
                           'gs_probackup add-instance -B backup-path -D '
                           'pgdata-path --instance=instance_name',
                           '[-E external-directories-paths]',
                           '[--remote-proto=protocol] '
                           '[--remote-host=destination]',
                           '[--remote-path=path] [--remote-user=username]',
                           '[--remote-port=port] [--ssh-options=ssh_options]',
                           '[--remote-libpath=libpath]',
                           '[--help]', '',
                           'gs_probackup del-instance -B backup-path '
                           '--instance=instance_name',
                           '[--help]', '',
                           'gs_probackup set-config -B backup-path '
                           '--instance=instance_name',
                           '[-D pgdata-path] [-E external-directories-paths]',
                           '[--archive-timeout=timeout]',
                           '[--retention-redundancy=retention-redundancy]',
                           '[--retention-window=retention-window]',
                           '[--wal-depth=wal-depth]',
                           '[--compress-algorithm=compress-algorithm]',
                           '[--compress-level=compress-level]',
                           '[-d dbname] [-h host] [-p port] [-U username]',
                           '[--log-level-console=log-level-console]',
                           '[--log-level-file=log-level-file]',
                           '[--log-filename=log-filename]',
                           '[--error-log-filename=error-log-filename]',
                           '[--log-directory=log-directory]',
                           '[--log-rotation-size=log-rotation-size]',
                           '[--log-rotation-age=log-rotation-age]',
                           '[--remote-proto=protocol] '
                           '[--remote-host=destination]',
                           '[--remote-path=path] [--remote-user=username]',
                           '[--remote-port=port] [--ssh-options=ssh_options]',
                           '[--remote-libpath=libpath]',
                           '[--help]', '',
                           'gs_probackup set-backup -B backup-path '
                           '--instance=instance_name -i backup-id',
                           '[--note=text] [--ttl=interval] '
                           '[--expire-time=time]',
                           '[--help]',
                           '',
                           'gs_probackup show-config -B backup-path '
                           '--instance=instance_name',
                           '[--format=plain|json]', '[--help]', '',
                           'gs_probackup show -B backup-path',
                           '[--instance=instance_name [-i backup-id]]',
                           '[--archive] [--format=plain|json]', '[--help]',
                           '',
                           'gs_probackup backup -B backup-path '
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
                           '[-d dbname] [-h host] [-p port] [-U username] '
                           '[-w] [-W password]',
                           '[-t rwtimeout]',
                           '[--remote-proto=protocol] '
                           '[--remote-host=destination]',
                           '[--remote-path=path] [--remote-user=username]',
                           '[--remote-port=port] [--ssh-options=ssh_options]',
                           '[--ttl=interval] [--expire-time=time]',
                           '[--backup-pg-replslot]',
                           '[--help]',
                           '',
                           'gs_probackup restore -B backup-path '
                           '--instance=instance_name',
                           '[-D pgdata-path] [-i backup-id] '
                           '[-j threads_num] [--progress]',
                           '[--force] [--no-sync] [--no-validate] '
                           '[--skip-block-validation]',
                           '[--external-mapping=OLDDIR=NEWDIR] '
                           '[-T OLDDIR=NEWDIR]',
                           '[--skip-external-dirs] [-I incremental_mode]',
                           '[--recovery-target-time=time|'
                           '--recovery-target-xid=xid',
                           '|--recovery-target-lsn=lsn|'
                           '--recovery-target-name=target-name]',
                           '[--recovery-target-inclusive=boolean]',
                           '[--remote-proto=protocol] '
                           '[--remote-host=destination]',
                           '[--remote-path=path] '
                           '[--remote-user=username]',
                           '[--remote-port=port] '
                           '[--ssh-options=ssh_options]',
                           '[--log-level-console=log-level-console]',
                           '[--log-level-file=log-level-file]',
                           '[--log-filename=log-filename]',
                           '[--error-log-filename=error-log-filename]',
                           '[--log-directory=log-directory]',
                           '[--log-rotation-size=log-rotation-size]',
                           '[--log-rotation-age=log-rotation-age]',
                           '[--help]',
                           '',
                           'gs_probackup merge -B backup-path '
                           '--instance=instance_name -i backup-id',
                           '[-j threads_num] [--progress]',
                           '[--log-level-console=log-level-console]',
                           '[--log-level-file=log-level-file]',
                           '[--log-filename=log-filename]',
                           '[--error-log-filename=error-log-filename]',
                           '[--log-directory=log-directory]',
                           '[--log-rotation-size=log-rotation-size]',
                           '[--log-rotation-age=log-rotation-age]',
                           '[--help]',
                           '',
                           'gs_probackup delete -B backup-path '
                           '--instance=instance_name',
                           '[-i backup-id | --delete-expired | '
                           '--merge-expired | --status=backup_status]',
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
                           '[--help]',
                           '',
                           'gs_probackup validate -B backup-path',
                           '[--instance=instance_name] [-i backup-id]',
                           '[-j threads-num] [--progress] '
                           '[--skip-block-validation]',
                           '[--recovery-target-time=time|'
                           '--recovery-target-xid=xid',
                           '|--recovery-target-lsn=lsn|'
                           '--recovery-target-name=target-name]',
                           '[--recovery-target-inclusive=boolean]',
                           '[--recovery-target-timeline=timeline]',
                           '[--log-level-console=log-level-console]',
                           '[--log-level-file=log-level-file]',
                           '[--log-filename=log-filename]',
                           '[--error-log-filename=error-log-filename]',
                           '[--log-directory=log-directory]',
                           '[--log-rotation-size=log-rotation-size]',
                           '[--log-rotation-age=log-rotation-age]',
                           '[--help]']

    def test_system_internal_tools(self):
        self.log.info('------------------显示帮助信息------------------')
        cmd_list = ['-?', '--help']
        for cmd in cmd_list:
            check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_probackup {cmd};
            '''
            self.log.info(check_cmd1)
            help_msg = self.PrimaryNode.sh(check_cmd1).result()
            self.log.info(help_msg)
            line_msg = help_msg.splitlines()
            for j in line_msg:
                self.log.info(j)
                self.assertIn(j.strip(), self.except_msg)

    def tearDown(self):
        # 无须清理环境
            self.log.info(f'-----{os.path.basename(__file__)} end-----')
