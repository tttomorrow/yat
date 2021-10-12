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

from yat.cli import git
from yat.cli.entry import cli
from yat.cli.env_checking import check_core_dump_setting
from yat.const import os
from yat.errors import YatError
from yat.suite import YatCommand, make_template, make_schedule


def parse_config(configs):
    """
    parse key=value command to map
    :param configs: the k-v pair list to parse
    :return: map of k-v pairs
    """
    res = {}
    for config in configs:
        idx = config.find('=')
        if idx == -1:
            raise YatError('parse config option %s failed' % config)
        k = config[:idx]
        v = config[idx + 1:]
        res[k] = v

    return res


def pre_check(strict):
    """
    check env core dump setting is valid
    """
    check_res = check_core_dump_setting()
    if len(check_res) > 0:
        print("yat suite check error:")
        for error in check_res:
            print("\t* {}".format(error))
        raise YatError("yat suite check failed")


@cli.command(name='suite', short_help='Test suite manager')
@click.argument("command", required=False, nargs=1, default='run',
                type=click.Choice(['run', 'bkfill', 'init', 'mkschd', 'debug', 'info']))
@click.option('-d', '--test-dir', type=str, default='.', help='Set the test suite/group path to run test')
@click.option('-s', '--schedule', type=str, help='Set the schedule file to schedule')
@click.option('-m', '--mode', type=click.Choice(['regress', 'compare', 'single', 'diff']),
              default='regress', help='Set the mode to run yat')
@click.option('-l', '--left', help='Set the left node to run test (only available in compare mode)')
@click.option('-r', '--right',  help='Set the right node to run test (only available in compare mode)')
@click.option('-t', '--target', help='Set the node to running test (available in regress and single mode)')
@click.option('-f', '--configure', help='Set the configure file to load')
@click.option('-p', '--prefix-run-shell', help='Set the shell script file to run before run yat')
@click.option('-i', '--macro', multiple=True, help='Set the macro to load')
@click.option('-n', '--nodes', help='Set the nodes configure file to load')
@click.option('-e', '--macro-file', help='Set the macro file to load')
@click.option('-c', '--config-opt', multiple=True, help='Set the configure to override')
@click.option('-o', '--output', help='Set the output path to generate results')
@click.option('-x', '--cases', help='Set the cases list to schedule')
@click.option('--width', help='Set the output report print-width')
@click.option('--bare', is_flag=True, help='Only show test case output')
@click.option('--report-server', is_flag=True, help='Start report service, after finished test')
@click.option('--force', is_flag=True, help='Force to execute action')
@click.option('--timeout', type=int, help='Set the timeout of test case')
@click.option('--daemon', is_flag=True, help='Run Yat in daemon mode')
@click.option('--color', is_flag=True, help='Print report with color')
@click.option('--lib-path', help='Set the jar library search path')
@click.option('--no-echo', is_flag=True, help='Do not echo sql text to output')
@click.option('--panic', is_flag=True, help='Panic when error or not')
@click.option('--suite-serial', is_flag=True, help='Running all the test in serial')
@click.option('--debug', is_flag=True, help='Running in debug module')
@click.option('--no-clean', is_flag=True, help='Do not clean the test suite before running')
@click.option('--git', help='Running the test suite or group in this git repo')
@click.option('--git-dir', help='Set the git clone directory(only available when --git supply)')
@click.option('--git-branch', help='Set the branch to checkout(only available when --git supply)')
@click.option('--git-sparse', multiple=True, help='Git sparse pattern')
@click.option('--expect', help='Set the expect sub directory')
@click.option('--strict', is_flag=True, help='if pre-check failed abort')
def suite(command, **opts):
    """
    Running test cases in suite

    \b
    yat suite [run]
    yat suite [run] [-d /path/to/suite/dir] [-o /path/to/suite/output/dir]
    yat suite [run] [-d /path/to/suite/dir] [-o /path/to/suite/output/dir] [-s /path/to/schedule/file]
    yat suite [run] [-m single|regress|compare]
    yat suite [run] [-d /path/to/suite/dir] [--color] [-o /path/to/suite/output/dir]
    yat suite [run] [-d /path/to/suite/dir] [--git git_repo] [-o /path/to/suite/output/dir]
        [--git-branch branch] [--git-dir dir]
        [--git-sparse sparse-pattern ...]

    \b
    yat suite init [-d /path/to/suite/dir] [-c key1=value1 ...] [--force]

    \b
    yat suite mkschd [-d /path/to/suite/dir] [--force]

    \b
    yat suite bkfill [-d /path/to/suite/dir] [--force] (not support now)
    """
    pre_check(opts['strict'])

    git_url = opts['git']
    test_dir = opts['test_dir']

    if git_url:
        git_dir = opts['git_dir'] if opts['git_dir'] else git.parse_dir(git_url)
        if not os.path.isabs(test_dir):
            test_dir = os.path.join(git_dir, test_dir)

        git.clone_or_fetch(git_url, repo=git_dir, branch=opts.get('git_branch'), sparse_list=opts.get('git_sparse'))

    opts['test_dir'] = os.path.abspath(test_dir)

    force = opts['force']

    if command == 'run':
        opts['action'] = 'run'
        ret = YatCommand(**opts).run()
        if not opts['bare'] and ret == 0:
            print("Run test suite finished")
        if opts['report_server']:
            pass
    elif command == 'init':
        config = parse_config(opts['config_opt'])
        make_template(test_dir, config, force=force)
        print("Initialize test suite finished")
    elif command == 'mkschd':
        make_schedule(test_dir, force)
        print("Make schedule file finished")
    elif command == 'bkfill':
        raise YatError("Not support now")
    elif command == 'debug':
        opts['action'] = 'debug'
        YatCommand(**opts).run()
    elif command == 'info':
        opts['action'] = 'info'
        YatCommand(**opts).run()
    else:
        raise YatError("action %s is not support" % command)


@cli.command()
def version():
    """
    Print version message
    """
    print(YatCommand().version())
