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
import stat
import click

from yat.cli.entry import cli
from yat.common.utils import scan_path
from yat.errors import YatError
from yat.suite import is_test_suite


class CollectHandler:
    def __init__(self, output, verbose=False):
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        self._diff = os.fdopen(os.open(os.path.join(output, 'yat.diff'), flags, mode), 'w')
        self._log = os.fdopen(os.open(os.path.join(output, 'yat.log'), flags, mode), 'w')
        self._json = os.fdopen(os.open(os.path.join(output, 'yat.json'), flags, mode), 'w')

        self._json.write("[\n")
        self._first = True
        self.verbose = verbose

    def __call__(self, path, is_dir, base):
        if is_dir and is_test_suite(path):
            if self.verbose:
                print('collecting result of %s ... ok' % path)
            diff = os.path.join(path, 'log', 'yat.diff')
            log = os.path.join(path, 'log', 'yat.log')
            json = os.path.join(path, 'log', 'yat.json')
            if os.path.exists(diff):
                self._diff.write(self.read(diff))
                self._diff.write('\n')

            if os.path.exists(log):
                self._log.write(self.read(log))

            if os.path.exists(json):
                if self._first:
                    self._json.write(self.read(json))
                    self._first = False
                else:
                    self._json.write(',\n')
                    self._json.write(self.read(json))

    def read(self, path):
        with open(path) as f:
            return f.read()

    def finishe(self):
        self._diff.close()
        self._log.close()
        self._json.write('\n]')
        self._json.close()


@cli.command(name='collect')
@click.option('-d', '--dir', required=True, help='The directory to scan suite', default='.')
@click.option('-o', '--output', help='The path to output', default='.')
@click.option('-v', '--verbose', is_flag=True, help='Show collect detail message')
def collect(dir, output, verbose):
    """
    Collect all result of suite to one
    """
    if os.path.exists(dir):
        handler = CollectHandler(output, verbose)
        try:
            scan_path(dir, handler, True)
        finally:
            handler.finishe()
    else:
        raise YatError('given path %s is not exists' % dir)
