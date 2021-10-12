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

from yat.guard.report import ConsoleReporter
from yat.guard.utils import script_valid, is_yat_suite, walk_path
from .basic_checker import BasicChecker


class PathChecker(BasicChecker):
    def __init__(self, src, reporter=ConsoleReporter(), **opts):
        super(PathChecker, self).__init__(src, reporter, **opts)
        self.yat = opts.get('yat', False)

    def check(self):
        self.success = True

        def yat_handler(path, is_dir):
            if is_dir and is_yat_suite(path):
                for root, dirs, files in os.walk(os.path.join(path, 'testcase')):
                    for script in files:
                        if script_valid(script):
                            self.success = self._check_script(os.path.join(root, script)) and self.success

        def normal_handler(path, is_dir):
            if not is_dir and script_valid(path):
                self.success = self._check_script(path) and self.success

        with self.reporter:
            walk_path(self.src, yat_handler if self.yat else normal_handler)
            return self.success
