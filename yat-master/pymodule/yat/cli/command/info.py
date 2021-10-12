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

from yat.const import YAT_HOME
from yat.suite.yat_commander import YatCommand
from ..entry import cli


@cli.command(name='info', short_help='Show current yat system information')
def info():
    print("Yat Test Framework")
    print("System Information list here:")
    print("    Yat home path: {}".format(YAT_HOME))
    print("    Yat version: {}".format(YatCommand().version()))
