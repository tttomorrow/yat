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
from yat.common.utils import scan_path, rmtree, chmod
from yat.suite import suite_permission, is_test_suite


def remove_path(path):
    """ do real remove of path tree """
    if os.path.exists(path):
        rmtree(path)


def cleanup_handler(path, is_dir, base):
    """ scan_path handler to deal with each path """
    if is_dir and is_test_suite(path):
        print('cleanup suite: %s' % path)
        suite_permission(path, True)
        chmod(path, 0o700)
        try:
            remove_path(os.path.join(path, 'log'))
            remove_path(os.path.join(path, 'temp'))
            remove_path(os.path.join(path, 'result'))
            for root, dirs, files in os.walk(os.path.join(path, 'testcase')):
                for f in files:
                    if f.endswith(".pyc"):
                        os.unlink(os.path.join(root, f))
                for d in dirs:
                    if d == '__pycache__':
                        chmod(root, 0o700)
                        remove_path(os.path.join(root, d))
        finally:
            suite_permission(path)


@cli.command(name='cleanup')
@click.option('-d', '--dir', help='Directory to scan and cleanup suite', default='.')
def cleanup(dir):
    """
    Cleanup all the suites in given directory
    """
    scan_path(dir, cleanup_handler, True)
