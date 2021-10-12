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

from yat.test.inject import RandomTestCase
from yat.test.inject import RandomInject
from yat.test.inject.decorator import order


class TestRandom(RandomTestCase):
    def test_001(self):
        pass

    @order(index=1)
    def test_002(self):
        pass

    def test_abc(self):
        pass

    def inject_001(self):
        pass

    def inject_002(self):
        pass

    def inject_003(self):
        pass

    def check_001(self):
        pass

    def check_002(self):
        pass

    @order(index=1)
    def check_003(self):
        pass


node = object()
inject = RandomInject(node)
functions = inject.run(TestRandom())

print(functions)
