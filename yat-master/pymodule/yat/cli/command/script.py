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

import click

from yat.cli.entry import cli
from yat.common.shell import run_shell
from yat.const import YAT_HOME_SCRIPT, YAT_HOME_PYTHON


@cli.command(name='script')
@click.argument('script', required=True, nargs=1)
@click.argument('args', nargs=-1)
def invoke_script(script, args):
    """
    Invoke script in yat script directory
    """
    os.environ['PATH'] = '%s:%s' % (YAT_HOME_SCRIPT, os.environ['PATH'])
    if 'PYTHONPATH' in os.environ:
        os.environ['PYTHONPATH'] = '%s:%s' % (YAT_HOME_PYTHON, os.environ['PYTHONPATH'])
    else:
        os.environ['PYTHONPATH'] = YAT_HOME_PYTHON

    run_shell('%s %s' % (script, ' '.join(args)), pipe=False)

