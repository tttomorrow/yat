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


@cli.command(name='services', short_help='Generate yat report with specific format')
@click.argument("services", required=False, nargs=1)
@click.argument("action", required=False, nargs=1)
@click.option('-d', '--test-dir', type=str, default='.', help='Set the test suite/group path to run test')
def yat_services(services, action, test_dir):
    """
    Run specific service of yat

    \b
    yat services <services_name> <action>

    """

