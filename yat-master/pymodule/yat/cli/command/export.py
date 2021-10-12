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

from yat.cli.entry import cli
from yat.errors import YatError
from yat.guard.errors import TestGuardError
from yat.guard.export import PathExporter


@cli.command(name='export', short_help='Export the test case information to dest')
@click.option('-s', '--src', help='The source to scan', default='.')
@click.option('-d', '--dest', help='The dest to export information', required=True)
@click.option('--append', is_flag=True, help='Append the export data to dest instead of override it')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output the exporting detail')
@click.option('--no-check', is_flag=True, help='Do not check meta, Just export')
@click.option('--not-yat', is_flag=True, help='the src is not Yat suite directory')
def export(src, dest, append, verbose, no_check, not_yat):
    """
    Export the test case information to dest

    \b
    valid dest url format:
        * db:zenith:username/password@host:port
        * file:excel:cida:/path/to/report.xlsx

    \b
    yat export [-s /path/to/suite/dir] -d <dest_url>
    yat export [-s /path/to/suite/dir] -d <dest_url> [--no-check]
    """
    try:
        PathExporter(src, dest, append=append, verbose=verbose, check=not no_check, yat=not not_yat).export()
        print('Export finished')
    except TestGuardError as e:
        raise YatError(str(e))
