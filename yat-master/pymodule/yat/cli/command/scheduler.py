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

import os
import time
from datetime import datetime

import click

from yat.cli import git
from yat.cli.entry import cli
from yat.common.file_lock import FileLock
from yat.errors import YatError
from yat.scheduler import Scheduler


@cli.command(name='schedule', short_help='Schedule shell or test suite from schedule file')
@click.option('-s', '--schedule', required=True, help='The schedule file to schedule')
@click.option('-l', '--log', help='Setting the log directory', default='-')
@click.option('-o', '--output', help='Set the output path to generate results')
@click.option('-d', '--source', type=str, default='.',
              help='Set the source suite scan path, default to path of schedule file')
@click.option('--width', help='Set the output report print-width', default='100')
@click.option('--color', is_flag=True, help='Print report color')
@click.option('--git', help='Running the test suite or group in this git repo')
@click.option('--git-dir', help='Set the git clone directory(only available when --git supply)')
@click.option('--git-branch', help='Set the branch to checkout(only available when --git supply)')
@click.option('--git-sparse', multiple=True, help='Git sparse pattern')
def yat_schedule(schedule, log, **opts):
    """
    Schedule shell or test suite from schedule file

    \b
    yat schedule -s /path/to/schedule.ys [--git git_repo] [--git-branch branch]
        [--git-sparse sparse-pattern ...] [--git-dir dir] [-o /path/to/output]
    yat schedule -s /path/to/schedule.ys [--git git_repo] [--git-branch branch]
        [--git-sparse sparse-pattern ...] [--git-dir dir] [-l /path/to/log/dir] [-o /path/to/output]
    """
    git_url = opts['git']
    if git_url:
        git_dir = opts['git_dir'] if opts['git_dir'] else git.parse_dir(git_url)
        if not os.path.isabs(schedule):
            schedule = os.path.join(git_dir, schedule)

        git.clone_or_fetch(git_url, repo=git_dir, branch=opts.get('git_branch'), sparse_list=opts.get('git_sparse'))

    if os.path.exists(schedule):
        lock_file = os.path.join(os.path.dirname(schedule), '.{}.lock'.format(os.path.basename(schedule)))
        try:
            with FileLock(lock_file):
                start_time = datetime.now()
                if log == '-':
                    Scheduler(path=schedule, width=opts['width'], color=opts['color']).schedule()
                else:
                    Scheduler(path=schedule, log_dir=log, width=opts['width'], color=opts['color']).schedule()
                end_time = datetime.now()

                duration = end_time - start_time
                print('Running all test using time: %s' % time.strftime('%Hh%Mm%Ss', time.gmtime(duration.total_seconds())))
        except OSError:
            raise YatError('Another yat is running maybe, stop now')
    else:
        raise YatError('the schedule file %s is not exists' % schedule)
