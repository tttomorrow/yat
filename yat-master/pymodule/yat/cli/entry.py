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

from yat.errors import YatError
from .env_checking import check_all


@click.group()
def cli():
    """
    Yat is yet another test framework

    \b
    yat suite [run|init|mkschd|bkfill] [-d /path/to/suite/dir]
        [-s /path/to/schedule.schd] [--color] [-m mode]
    yat schedule -s /path/to/schedule.ys
    yat backup [-d /path/to/suite/dirs] -b /path/to/backup/path [-m mode]
    yat cleanup [-d /path/to/suite/dirs]
    yat check [-s /path/to/check] [-d <report dest describe>]
    yat export [-s /path/to/check] [-d <report dest describe>]
    yat playbook [run|bkfill|gen] [-p /path/to/playbook.xls[x]]
    yat collect [-d /path/to/collect] [-o /path/to/output/dir]

    \b
    type yat [sub command] --help for more help information.

    """
    errors = check_all()
    if len(errors) > 0:
        print("The following checking is not pass:")
        for error in errors:
            print("    * {}".format(error))
        raise YatError("Checking Failed")
