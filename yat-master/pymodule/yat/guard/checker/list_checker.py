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

import sys

from yat.guard.report import ConsoleReporter
from .basic_checker import BasicChecker


class ListChecker(BasicChecker):
    def __init__(self, src, reporter=ConsoleReporter(), **opts):
        super(ListChecker, self).__init__(src, reporter, **opts)

    def check(self):
        self.success = True

        with self.reporter:
            if self.src == '-':
                stream = sys.stdin
            else:
                stream = open(self.src)

            for line in stream:
                line = line.strip('\n').strip('\r').strip(' ')
                if len(line) > 0:
                    self.success = self._check_script(line) and self.success
            if self.src != '-':
                stream.close()
            return self.success
