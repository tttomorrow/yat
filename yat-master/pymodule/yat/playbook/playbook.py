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

from .back_filler import PlaybookExpectBackFiller, PlaybookResultBackFiller
from .suite_generator import SuiteGenerator


class Playbook:
    def __init__(self, **kwargs):
        self.playbook = kwargs['playbook']
        self.suite_dir = kwargs['test_suite']
        self.opts = kwargs

    def generate_suite(self):
        SuiteGenerator(**self.opts).generate()

    def expect_back_fill(self):
        PlaybookExpectBackFiller(**self.opts).back_fill()

    def result_back_fill(self):
        PlaybookResultBackFiller(**self.opts).back_fill()
