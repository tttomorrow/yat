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

from yat.guard.checker.checkers import TestCaseChecker
from yat.guard.report import ConsoleReporter


class BasicChecker:
    def __init__(self, src, reporter=ConsoleReporter(), **opts):
        self.src = src
        self.reporter = reporter
        self.checkers = opts.get('checkers', None)
        self.case_checker = TestCaseChecker(self.checkers)
        self.verbose = opts.get('verbose', False)
        self.success = True
        self.filters = opts.get('filters', None)

    def _check_script(self, script):
        if self.verbose:
            sys.stdout.write('checking %s ...' % script)

        errors = None
        if self.filters:
            for ft in self.filters:
                if ft.match(script):
                    errors = self.case_checker.check(script)
            if errors is None:
                if self.verbose:
                    sys.stdout.write(' ignore\n')
                return True
        else:
            errors = self.case_checker.check(script)

        if len(errors) > 0:
            for err in errors:
                self.reporter.report(err)

            if self.verbose:
                sys.stdout.write(' er\n')
            return False
        else:
            if self.verbose:
                sys.stdout.write(' ok\n')
            return True

    def check(self):
        raise RuntimeError("you need override the check method")
