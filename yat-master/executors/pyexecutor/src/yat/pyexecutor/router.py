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
from .handler.statement import SqlHandler
from .handler.file import UnittestHandler, RunnableHandler
from .handler.vars import VarsHandler


router = [
    (r'^/statement/sql$', SqlHandler),
    (r'^/file/unittest$', UnittestHandler),
    (r'^/file/runnable$', RunnableHandler),
    (r'^/vars$', VarsHandler)
]
