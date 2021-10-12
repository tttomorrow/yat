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

from types import MethodType


class RandomInject:
    def __init__(self, node):
        self.node = node

    def run(self, case):
        return self._parse_case(case)

    def _parse_case(self, case):
        test_cases = []
        test_cases_order = []
        inject_cases = []
        inject_cases_order = []
        checkers = []
        checkers_order = []

        for name in dir(case):
            if name.startswith('test'):
                self._parse_fun(getattr(case, name), test_cases, test_cases_order)
            elif name.startswith('inject'):
                self._parse_fun(getattr(case, name), inject_cases, inject_cases_order)
            elif name.startswith('check'):
                self._parse_fun(getattr(case, name), checkers, checkers_order)

        test_cases_ordered, inject_cases_ordered, checkers_ordered = self._sort(
            test_cases_order, inject_cases_order, checkers_order)

        return test_cases_ordered + test_cases, inject_cases_ordered + inject_cases, checkers_ordered + checkers

    @staticmethod
    def _parse_fun(fun, cases, cases_order):
        if isinstance(fun, (MethodType,)):
            if hasattr(fun, '__order__'):
                cases_order.append(fun)
            else:
                cases.append(fun)

    @staticmethod
    def _sort(test_cases, inject_cases, checkers):
        return (sorted(test_cases, key=lambda i: i.order),
                sorted(inject_cases, key=lambda i: i.order),
                sorted(checkers, key=lambda i: i.order))
