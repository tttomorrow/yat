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

from yat.guard.setting import ctx
from .manager import checker
from ..errors import CheckError


@checker
class CaseNameChecker:
    """
    test case name checker
    """
    name = 'case_size_checker'

    def __init__(self):
        self.max_line = ctx.case_size_checker['max_line']
        self.max_size = ctx.case_size_checker['max_size']

    def check(self, script):
        errors = []
        if os.path.getsize(script) > self.max_size:
            errors.append(CheckError.error(
                CheckError.CHECK_ERROR,
                self.name,
                'file size out of limit',
                'test case file {}\'s size is bigger than the max value({})'.format(script, self.max_size),
                script
            ))

        with open(script, buffering=1000000, encoding='utf-8', errors='ignore') as case:
            count = 0
            for _ in case:
                count += 1

                if count > self.max_line:
                    errors.append(CheckError.error(
                        CheckError.CHECK_ERROR,
                        self.name,
                        'file line out of limit',
                        'test case file {}\'s line size is bigger than the max value({})'.format(script, self.max_line),
                        script
                    ))
                    break

        return errors
