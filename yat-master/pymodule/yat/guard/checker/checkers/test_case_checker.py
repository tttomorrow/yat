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

from yat.guard.errors import TestGuardError
from yat.guard.parser import MetaParseError, NotSupportScriptError
from yat.guard.setting import ctx
from .manager import all_checkers
from ..errors import CheckError


class TestCaseChecker:
    """ check one test case """
    name = "test_case_checker"

    def __init__(self, checkers=None):
        checker_list = checkers if checkers else ctx.checkers
        self.checker_map = all_checkers()
        self.checkers = checker_list if checker_list else all_checkers().keys()

    def check(self, script):
        script = os.path.abspath(script)
        message = []
        if not os.path.exists(script):
            return [CheckError.error(
                CheckError.PARSE_ERROR, self.name, 'file not exists', '{} is not exists'.format(script), script
            )]

        for name in self.checkers:
            checker = self.checker_map.get(name)
            if checker is None:
                raise TestGuardError('given checker name {} is not found'.format(name))
            try:
                message.extend(checker.check(script))
            except MetaParseError as e:
                message.append(CheckError.error(
                    CheckError.PARSE_ERROR, name, 'meta parse error', str(e), script)
                )
            except NotSupportScriptError:
                message.append(CheckError.warning(
                    CheckError.PARSE_ERROR, name, 'not support file type', 'not support file type found', script)
                )

        return message
