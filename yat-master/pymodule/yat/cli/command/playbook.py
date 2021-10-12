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
import shutil

import click

from yat.cli.entry import cli
from yat.common.path_searcher import PathSearch
from yat.common.utils import rmtree, chmod
from yat.errors import YatError
from yat.playbook import Playbook, PlaybookError
from .suite import suite

default_setting = {
    'yat.limit.case.size.max': '200K',
    'yat.limit.case.count.max': 100000,
    'yat.limit.case.depth.max': 2,
    'yat.limit.case.name.pattern': "'.*'"
}


def generate_suite(ctx, **opts):
    config = ['%s=%s' % (k, v) for k, v in default_setting.items()]
    config.extend(opts['config'])
    test_dir = opts['test_suite']

    ctx.invoke(suite, command='init', test_dir=test_dir, config_opt=config, force=True)
    if opts['nodes']:
        shutil.copy(opts['nodes'], os.path.join(test_dir, 'conf', 'nodes.yml'))

    try:
        Playbook(**opts).generate_suite()
    except PlaybookError as e:
        if os.path.exists(test_dir):
            chmod(test_dir, 0o700, True)
            rmtree(test_dir)
        raise YatError(e.message)


def run_suite(ctx, **opts):
    ctx.invoke(suite, command='run', test_dir=opts['test_suite'])


def back_fill(**opts):
    Playbook(**opts).expect_back_fill()


def result_back_fill(**opts):
    Playbook(**opts).result_back_fill()


def parse_playbook(playbook_dest):
    if playbook_dest is None:
        playbook_dest = PathSearch('.').search('playbook.xls', 'playbook.xlsx')

    if playbook_dest is None:
        raise YatError("given playbook %s is not exists" % playbook_dest)

    splits = playbook_dest.split(':')
    if len(splits) == 2:
        return splits[0], splits[1]
    elif len(splits) == 1:
        return 'tmss', splits[0]
    else:
        raise YatError("given playbook %s is illegal" % playbook_dest)


@cli.command(short_help='Yat playbook manager and runner')
@click.argument("command", required=False, nargs=1, default='run', type=click.Choice(['gen', 'bkfill', 'run']))
@click.option('-a', '--action', type=click.Choice(['gen', 'bkfill', 'run']), help='Set the action to do')
@click.option('-f', '--force', is_flag=True, help='Force replace origin playbook file')
@click.option('-v', '--verbose', is_flag=True, help='Print the verbose of detail')
@click.option('-p', '--playbook', help='Setting the playbook path to load')
@click.option('-d', '--test-suite', help='Setting the path to generate test suite directory')
@click.option('-n', '--nodes', help='Set the nodes configure file')
@click.option('-c', '--config', multiple=True, help='Set the configure to override')
@click.option("-s", '--start-sheet', type=int, help='Set the start index of sheet to generate', default=1)
@click.pass_context
def playbook(ctx, command, **opts):
    """
    Yat playbook manager and runner

    \b
    yat playbook [run] -p <playbook dest> [-d /path/to/generate/test-suite]
    yat playbook [run] -p /path/to/playbook.xls[x] [-d /path/to/generate/test-suite]
    yat playbook bkfill -p /path/to/playbook.xls[x] [-d /path/to/generate/test-suite]
    yat playbook gen -p /path/to/playbook.xls[x] [-d /path/to/generate/test-suite]

    \b
    playbook dest format:
        * poc:/path/to/playbook.xls[x]
        * tmss:/path/to/playbook.xls[x] default
    """
    action = opts['action']
    if action:
        print("!!! Warning: yat suite -a [action] is deprecated, and will be remove in the future. !!!")
        print("Instead of using: yat playbook [run]")

    if action is None and command:
        action = command

    playbook_dest = opts['playbook']

    schema, playbook_path = parse_playbook(playbook_dest)
    opts['playbook_schema'] = schema
    opts['playbook'] = playbook_path

    if opts['test_suite'] is None:
        opts['test_suite'], _ = os.path.splitext(os.path.basename(playbook_path))

    if action == 'bkfill':
        back_fill(**opts)
    else:
        generate_suite(ctx, **opts)
        if action == 'run':
            run_suite(ctx, **opts)
            result_back_fill(**opts)
