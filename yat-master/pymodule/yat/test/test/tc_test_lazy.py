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

from unittest import TestCase

from yat.test.node.node import LazyResource


class TestTarget:
    def hello(self):
        return "hello"

    def close(self):
        pass


class TestLazy(TestCase):
    def test_lazy(self):
        lazy = LazyResource(lambda: TestTarget())
        self.assertEqual(lazy.hello(), "hello")
        lazy.reset()
        lazy.reset()
        self.assertEqual(lazy.hello(), "hello")
