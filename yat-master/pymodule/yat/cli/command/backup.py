#!/usr/bin/env python
# encoding=utf-8
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

import click

from yat.backup import backup
from yat.cli.entry import cli
from yat.errors import YatError


@cli.command(name='backup', short_help='Backup last running result')
@click.option('-a', '--action', help='Action to do', required=True, type=click.Choice(['backup', 'init', 'config']))
@click.option('-d', '--dir', help='Directory to scan and backup suite', default='.')
@click.option('-m', '--mode', type=click.Choice(['full', 'quick', 'log']), help='Backup mode to using', default='quick')
@click.option('-b', '--backup-dir', help='Set the backup directory')
@click.option('-c', '--config', help='Set the config content[key=value]')
def backup_cli(action, **opts):
    """
    Backup last running result

    \b
    yat backup [-d /path/to/suite/dirs] [-m mode] -b /path/to/backup/dir
    """
    if action == 'backup':
        backup.do_backup(**opts)
    elif action == 'init':
        backup.do_init(**opts)
    elif action == 'config':
        backup.do_config(**opts)
    else:
        raise YatError('error: unknown value for -a/--action')
