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
from yat.upload import do_upload


@cli.command(name='upload', short_help='Upload test results to report center')
@click.option('-d', '--test-dir', help='the test suite directory', required=True, default='.')
@click.option('--tag', help='Set the tag to upload the test result')
@click.option('-n', '--name', help='Set the name of object under test')
@click.option('-v', '--version', help='Set the version of object under test')
@click.option('-c', '--csv-version', help='Set the CSV version of object under test')
def upload_cli(**opts):
    """
    Upload test case result to report center

    \b
    yat upload -d <test_dir> -n <target_name> -v <target_version> -c <target_csv_version>
    """
    do_upload(opts['test_dir'], **opts)
