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
import stat
from unittest import TestLoader, TextTestResult


class WritelnDecorator:
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, item):
        return getattr(self.stream, item)

    def writeln(self, msg=None):
        if msg is not None:
            self.write(msg)
        self.write('\n')


class UnittestExecutor:
    loader = TestLoader()

    @staticmethod
    def _print_detail(output, typing, cases):
        output.writeln("=================================== %s test cases ===================================" % typing)
        i = 1
        for test, detail in cases:
            output.writeln("+---> ({}) {} <---".format(i, test))
            i += 1
            for line in detail.splitlines():
                output.writeln("|    %s" % line)
            output.writeln("|")

    def execute(self, case, out, log):
        class_name = case.replace('/', '.')
        suite = self.loader.loadTestsFromName(class_name)
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        with os.fdopen(os.open(out, flags, mode), 'w') as output:
            output_ln = WritelnDecorator(output)
            result = TextTestResult(output_ln, True, 2)
            for case in suite:
                print(case)
                print(type(case))
                for t in case:
                    print(t)
                    print(type(t))

            suite.run(result)
            self.print_error(result, output_ln)

        return result

    def print_error(self, result, output):
        if len(result.skipped) > 0:
            self._print_detail(output, "Skipped", result.skipped)

        if len(result.failures) > 0:
            self._print_detail(output, "Failures", result.failures)

        if len(result.errors) > 0:
            self._print_detail(output, "Errors", result.errors)
