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

from .parser import MetaParser, MetaParseError
from .setting import ctx


def get_comment_mark(script):
    _, ext = os.path.splitext(script)

    return ctx.valid_case.get(ext)


def get_second_ext():
    return ctx.second_ext


def script_valid(script):
    return get_comment_mark(script) is not None


def try_parse_meta(script, line_mark, multiline_mark):
    exception = None
    for charset in ctx.valid_charset:
        try:
            with open(script, encoding=charset) as fscript:
                return MetaParser(fscript, line_mark, multiline_mark).parse()
        except UnicodeDecodeError as e:
            exception = e

    raise MetaParseError("try to parse script {} with all charset {}, but failed".format(
        script, ctx.valid_charset
    )) from exception


def walk_path(path, handler, include_self=True):
    def _walk_path(_path, _handler):
        for sub_dir in os.listdir(_path):
            real_path = os.path.join(_path, sub_dir)
            if os.path.isdir(real_path):
                is_dir = True
            else:
                is_dir = False

            _handler(real_path, is_dir)
            if is_dir:
                _walk_path(real_path, handler)

    if os.path.isdir(path):
        if include_self:
            handler(path, True)
        _walk_path(path, handler)
    else:
        if include_self:
            handler(path, False)


def is_yat_suite(path):
    conf_dir = os.path.join(path, 'conf')
    if not os.path.exists(conf_dir):
        return False
    if not os.path.exists(os.path.join(path, 'testcase')):
        return False

    return True
