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
import sys
from unittest import TestLoader, TextTestResult

loader = TestLoader()


def set_test_suite_dir(suite_dir, lib_dir):
    sys.path.append(suite_dir)
    if lib_dir:
        for lib in lib_dir:
            if os.path.exists(lib):
                sys.path.append(lib)


class WritelnDecorator:
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, item):
        return getattr(self.stream, item)

    def writeln(self, msg=None):
        if msg is not None:
            self.write(msg)
        self.write('\n')


def run_test_case(name):
    name = name.replace('/', '.')
    suite = loader.loadTestsFromName(name)

    result = TextTestResult(WritelnDecorator(sys.stdout), True, 2)
    suite.run(result)

    return result
