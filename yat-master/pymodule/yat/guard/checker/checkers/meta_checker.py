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

"""
check the basic restrict

1. the meta item required and not allow empty: @owner, @date, @describe, @requirement, @developer
2. the owner of @owner, developer of @developer, dts number and fix owner of @dts are basic legal

"""
import re
from datetime import date

from yat.guard.setting import ctx
from yat.guard.utils import get_comment_mark, try_parse_meta
from .manager import checker
from ..errors import CheckError


@checker
class CaseMetaChecker:
    """
    test case meta checker
    """
    name = 'case_meta_checker'

    def __init__(self):
        self.meta_checker = ctx.meta_checker

    @staticmethod
    def one_match(regex, value):
        for reg in regex:
            if reg.match(value):
                return True
        return False

    def check(self, script):
        errors = []

        mark = get_comment_mark(script)
        if mark is None:
            return [CheckError.warning(
                CheckError.PARSE_WARNING, self.name,
                'not support file type',
                '{} is not a valid script'.format(script),
                script
            )]
        line_mark, multiline_mark = mark
        meta = try_parse_meta(script, line_mark, multiline_mark)

        for name, _ctx in self.meta_checker.items():
            if _ctx['required']:
                if name in meta:
                    errors.extend(self.check_common(name, meta, _ctx['checker'], meta[name]))
                else:
                    errors.append(
                        CheckError.error(
                            CheckError.CHECK_ERROR,
                            self.name,
                            'meta require miss',
                            '@{} is required'.format(name),
                            meta.script
                        )
                    )
            else:
                if name in meta:
                    errors.extend(self.check_common(name, meta, _ctx['checker'], meta[name]))

        return errors

    def check_common(self, name, meta, checker, meta_value):
        errors = []
        if isinstance(meta_value, (list, tuple)):
            for _value in meta_value:
                if not self.check_one_value(_value, checker):
                    errors.append(
                       CheckError.error(
                           CheckError.CHECK_ERROR,
                           self.name,
                           'meta value invalid',
                           'value {} of @{} is invalid'.format(_value, name),
                           meta.script
                       )
                    )
        elif isinstance(meta_value, date):
            if not self.check_one_value(meta_value, checker):
                errors.append(
                    CheckError.error(
                        CheckError.CHECK_ERROR,
                        self.name,
                        'meta value invalid',
                        'value {} of @{} is invalid'.format(meta_value, name),
                        meta.script
                    )
                )
        return errors

    def check_one_value(self, meta_value, checker):
        if checker is None:
            return True

        if isinstance(checker, (list, tuple)):
            for _checker in checker:
                if self.check_one_checker(meta_value, _checker):
                    return True
            return False
        else:
            return self.check_one_checker(meta_value, checker)

    def check_one_checker(self, meta_value, checker):
        if type(checker) in (type(u''), type(b'')):
            return re.match(checker, meta_value) is not None
        elif callable(checker):
            return checker(meta_value)
        else:
            return checker.match(meta_value)

