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

from . import runner


# print the error detail with format
def _print_detail(typing, cases):
    print("=================================== %s test cases ===================================" % typing)
    i = 1
    for test, detail in cases:
        print("+---> ({}) {} <---".format(i, test))
        i += 1
        for line in detail.splitlines():
            print("|    %s" % line)
        print("|")


@click.command()
@click.option('-d', '--test-suite', required=True, help='Set the test suite directory')
@click.option('-l', '--library', help='Set the library directory', multiple=True)
@click.option('-t', '--test-case', required=True, help='Set the test case name to run')
def cli(**opts):
    """
    run python test write with unittest format
    """
    test_suite_dir = opts['test_suite']
    if not os.path.exists(test_suite_dir):
        print('test case directory %s is not exists' % test_suite_dir)
        exit(1)

    runner.set_test_suite_dir(test_suite_dir, opts['library'])
    result = runner.run_test_case(opts['test_case'])

    if len(result.skipped) > 0:
        _print_detail("Skipped", result.skipped)

    if len(result.failures) > 0:
        _print_detail("Failures", result.failures)

    if len(result.errors) > 0:
        _print_detail("Errors", result.errors)

    if not result.wasSuccessful():
        exit(1)
