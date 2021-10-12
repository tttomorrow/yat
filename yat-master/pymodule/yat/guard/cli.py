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

import sys

import click

from yat.guard import get_reporter
from yat.guard.checker import PathChecker
from yat.guard.export import PathExporter
from .errors import TestGuardError

__level_map = {
    'info': LEVEL_INFO,
    'warn': LEVEL_INFO,
    'error': LEVEL_ERROR
}


@click.group()
def cli():
    """
    tguard tools to scan and analyze test case's meta message, and additional work on it

    \b
    python tguard.pyz check -s /path/to/test/case -d file:text:/path/to/report.txt
    python tguard.pyz export -s /path/to/test/case -d file:excel:cida:/path/to/report.xlsx
    """
    pass


@cli.command(short_help='Checking test cases')
@click.option('-s', '--src', help='Set the search directory', default='.')
@click.option('-d', '--dest', help='Set the export information', default="file:text:report.txt")
@click.option('-l', '--level', help='Set the level of checking', type=click.Choice(['info', 'warn', 'error']), default='warn')
@click.option('--lib', help='Setting additional python search path(For DB driver)', default='.')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output the checking detail')
@click.option('--yat', is_flag=True, help='the src is Yat suite directory')
def check(src, dest, level, lib, verbose, yat):
    """
    Checking test cases, and report to dest

    \b
    valid dest format:
        * file:text:/path/to/report.txt
        * file:excel:/path/to/report.xlsx
        * file:json:/path/to/report.json
        * db:zenith:username/password@host:port
    """
    sys.path.append(lib)
    reporter = get_reporter(dest)
    if reporter is None:
        raise TestGuardError("can not found reporter with given url: %s" % dest)

    success = PathChecker(src, reporter, verbose=verbose, yat=yat).check()

    if success:
        print('Checking Passed')
    else:
        print('Checking Not Passed')


@cli.command(short_help='Export the test case information to dest')
@click.option('-s', '--src', help='The source to scan', default='.')
@click.option('-d', '--dest', help='The dest to export information', required=True)
@click.option('--append', is_flag=True, help='Append the export data to dest instead of override it')
@click.option('--lib', help='Setting additional python search path(For DB driver)', default='.')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output the exporting detail')
@click.option('--no-check', is_flag=True, help='Do not check meta, Just export')
@click.option('--yat', is_flag=True, help='the src is Yat suite directory')
def export(src, dest, append, lib, verbose, no_check, yat):
    """
    Export the test case information to dest

    \b
    valid dest format:
        * db:zenith:username/password@host:port
        * file:excel:cida:/path/to/report.xlsx
    """
    sys.path.append(lib)
    PathExporter(src, dest, append=append, verbose=verbose, check=not no_check, yat=yat).export()
    print('Export finished')
