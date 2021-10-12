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

import abc
import difflib
import re
from abc import ABC


class YatResult(ABC):
    """
    abstract base class of all the result with compare methods
    """

    def __init__(self, result):
        self._result = result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.success()

    @abc.abstractmethod
    def success(self):
        pass

    def ors(self, *or_operators):
        """
        raise error if all operation failed

        YatResult.ors(
            ('expect',
                (0, 1, 2),
                (2, 2, 2),
                (2, 3, 3)
            ),
            ('success', )
        )
        :param or_operators: tuple operation which like this ('operation name', param1, param2, ...)
        """
        errors = []
        for operate in or_operators:
            if len(operate) < 1:
                raise RuntimeError("each operator must last one value")
            operate_name, *operate_args = operate
            try:
                getattr(self, operate_name)(*operate_args)
                return
            except AssertionError as e:
                errors.append(e)

        return self._failed('failed in or operators and all the error: \n{}', '\n'.join((str(e) for e in errors)))

    def ands(self, *and_operators):
        """
        raise error if at lest one operation failed

        YatResult.ands(
            ('expect',
                (0, 1, 2),
                (2, 2, 2),
                (2, 3, 3)
            ),
            ('success', )
        )
        :param and_operators: tuple of operation which like this ('operation name', param1, param2, ...)
        :return:
        """
        for operate in and_operators:
            if len(operate) < 1:
                raise RuntimeError("each operator must last one value")
            operate_name, *operate_args = operate
            try:
                getattr(self, operate_name)(*operate_args)
            except AssertionError as e:
                self._failed('failed in and operators and the error: {}', str(e))

    @staticmethod
    def _failed(msg, *args, **kwargs):
        if len(args) == 0:
            if len(kwargs) == 0:
                raise AssertionError(msg)
            else:
                raise AssertionError(msg.format(**kwargs))
        else:
            raise AssertionError(msg.format(*args))

    def result(self):
        return self._result


class SqlResult(YatResult):
    def __init__(self, result=None, error=None):
        super(SqlResult, self).__init__(result)
        self._error = error if error is None else error.strip('\r\n\t ')
        self._check_input()

    def _check_input(self):
        if self._result is not None and self._error is not None:
            raise RuntimeError('result and error can not be show at the same time')

    def result(self):
        return self._result if self._result else self._error

    def success(self):
        if self._error is not None:
            self._failed("execute sql failed with error message: {}".format(self._error))

    def expect(self, *expect):
        if self._error is not None:
            real_result = [self._error + '\n']
        else:
            real_result = self._fetch_text_result(self._result)

        real_expect = self._fetch_text_result(expect)

        self._diff(real_expect, real_result)

    def expect_order(self, *expect):
        if self._error is not None:
            real_result = [self._error + '\n']
        else:
            real_result = sorted(self._fetch_text_result(self._result))

        real_expect = sorted(self._fetch_text_result(expect))

        self._diff(real_expect, real_result)

    @staticmethod
    def _fetch_text_result(result):
        res = []
        for row in result:
            if isinstance(row, (tuple, list)):
                res.append(','.join([str(v) for v in row]) + '\n')
            else:
                res.append(str(row) + '\n')
        return res

    def _diff(self, expect, result):
        diff = difflib.context_diff(expect, result, fromfile='expect', tofile='result')
        diff = ''.join(diff)
        if len(diff) > 0:
            self._failed("test failed:\n{}", diff)

    def error(self, err_msg):
        if self._result is not None:
            self._failed('expect sql get error but success, and the result is:\n{}', self._result)

        real_result = [self._error]
        real_expect = [err_msg + '\n']

        self._diff(real_expect, real_result)

    def contains(self, contains):
        if self._error is not None:
            self._failed("execute sql failed:\n{}\nbut expect result contains:\n{}".format(
                self._error,
                str(contains)
            ))

        if isinstance(contains, (tuple, list)):
            for line in self._result:
                if self._list_compare(contains, line):
                    return

            self._failed("{} not contains in {}".format(contains, self._result))
        else:
            for line in self._result:
                for row in line:
                    if contains == row:
                        return

            self._failed("{} not contains in {}".format(contains, self._result))

    def regex(self, regex):
        if self._error is not None:
            self._failed("execute sql failed:\n{}\nbut expect result match regex:\n{}".format(
                self._error,
                regex
            ))

        if isinstance(regex, (str,)):
            regex = re.compile(regex)

        for line in self._result:
            for row in line:
                if regex.match(str(row)):
                    return
        self._failed("regex {} not match the result {}".format(regex, self._result))

    def rows(self, expect_row):
        if self._error is not None:
            self._failed("expect {} rows result, but get error: {}", expect_row, self._error)

        if len(self._result) != expect_row:
            self._failed("expect {} rows result, but get {} rows", expect_row, len(self._result))

    @classmethod
    def _list_compare(cls, a, b):
        iter_b = iter(b)

        for v_a in a:
            try:
                v_b = next(iter_b)
            except StopIteration:
                return False
            if v_a != v_b:
                return False

        return True


class ShellResult(YatResult):
    """
       shell result specific implements
    """

    def __init__(self, result, return_code):
        super(ShellResult, self).__init__(result.strip('\r\n\t '))
        self._return_code = return_code

    def expect(self, expect):
        if self._result != expect:
            self._failed("{} != {}", self._result, expect)

    def contains(self, contains):
        if contains not in self._result:
            self._failed("{} not contains {}", self._result, contains)

    def regex(self, regex):
        if isinstance(regex, (str,)):
            regex = re.compile(regex)

        if regex.match(self._result) is None:
            self._failed("regex {} not match the result {}", regex, self._result)

    def code(self, expect_code):
        if expect_code != self._return_code:
            self._failed("command return code {} != {}".format(self._return_code, expect_code))

    def not_code(self, not_expect_code):
        if not_expect_code == self._return_code:
            self._failed("command return code {} == {}".format(self._return_code, not_expect_code))

    def success(self):
        if self._return_code != 0:
            self._failed("run command return error code: {}".format(self._return_code))

    def return_code(self):
        return self._return_code
