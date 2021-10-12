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
import re

import click

from yat.cli.entry import cli
from yat.errors import YatError
from yat.guard.checker import PathChecker, ListChecker
from yat.guard.checker import all_checkers
from yat.guard.errors import TestGuardError
from yat.guard.report import get_reporter, CombineReporter
from yat.guard.setting import load


@cli.command(name='check', short_help='Checking test cases')
@click.option('-c', '--configure', help='Set the checker configure file')
@click.option('-s', '--src', help='Set the source directory or file, default is .')
@click.option('-l', '--check-list', help='Set the checking list file')
@click.option('-d', '--dest', multiple=True, help='Set the export information, default is report.txt',
              default=["file:text:report.txt"])
@click.option('--level', help='Set the level of checking', type=click.Choice(['info', 'warn', 'error']),
              default='warn')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output the checking detail')
@click.option('--not-yat', is_flag=True, help='the src is not Yat suite directory')
@click.option('-e', '--filters', multiple=True, help='Set the filter to filter file to check')
@click.option('-r', '--checkers', help='Set the checker list to use')
@click.option('--list-checkers', help='List all checkers', is_flag=True)
def check(configure, src, check_list, dest, level, verbose, not_yat, filters, checkers, list_checkers):
    """
    Checking test cases, and report to dest

    \b
    valid dest url format:
        * file:text:/path/to/report.txt
        * file:excel:/path/to/report.xlsx
        * file:json:/path/to/report.json
        * file:html:/path/to/report.html
        * db:zenith:username/password@host:port

    \b
    check list file is a file contents list of file path, which is split with '\\n'
    valid list file can be a txt file or -, which means stand input

    \b
    yat check [-c /path/to/configure/path ] [-s /path/to/suite/dir] -d <dest_url>
    yat check [-c /path/to/configure/path ] [-s /path/to/suite/dir] -d <dest_url> [--not-yat]
    yat check [-c /path/to/configure/path ] [-s /path/to/suite/dir] -d <dest_url> [--not-yat] [-e '^.*/testcase/.*\\.(sh|sql|py|go)' ...]
    """
    try:
        if list_checkers:
            for name in all_checkers().keys():
                print("\t{}".format(name))
            return
        reporters = []
        for single_dest in dest:
            reporter = get_reporter(single_dest)
            if reporter is None:
                raise YatError("can not found reporter with given url: %s" % single_dest)
            reporters.append(reporter)

        reporter = CombineReporter(*reporters)

        if src is None and check_list is None:
            src = '.'

        if src is not None and check_list is not None:
            raise YatError('-s/--src or -l/--check-list is mutual exclusion, choose one to begin the check')

        filters = _make_filters(filters)

        if configure:
            load(configure)

        if checkers:
            checkers = checkers.split(',')

        if src:
            success = PathChecker(
                src, reporter,
                verbose=verbose, yat=not not_yat,
                filters=filters, checkers=checkers).check()
        else:
            success = ListChecker(
                check_list, reporter,
                verbose=verbose, filters=filters,
                checkers=checkers).check()

        if success:
            print('Checking Passed')
        else:
            raise YatError('Checking Not Passed')
    except TestGuardError as e:
        raise YatError(str(e))


def _make_filters(filters):
    if len(filters) == 0:
        return None
    else:
        return [re.compile(it) for it in filters]
