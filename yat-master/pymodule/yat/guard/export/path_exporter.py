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
import sys

from yat.guard.checker import CaseMetaChecker
from yat.guard.errors import TestGuardError
from yat.guard.parser import MetaParseError, NotSupportScriptError
from yat.guard.utils import script_valid, get_comment_mark, is_yat_suite, walk_path, try_parse_meta
from .storage_manager import get_storage


class PathExporter:
    name = "path_exporter"

    def __init__(self, src, dest, **opts):
        self.src = src
        self.storage = get_storage(dest, **opts)
        if self.storage is None:
            raise TestGuardError('no suitable storage found for url %s' % dest)

        self.check = opts.get('check', True)
        self.yat = opts.get('yat', False)
        self.verbose = opts.get('verbose', False)

    def _store(self, script):
        mark = get_comment_mark(script)
        if mark is None:
            return
        try:
            if self.verbose:
                sys.stdout.write('exporting %s ...' % script)

            line_mark, multiline_mark = mark
            meta = try_parse_meta(script, line_mark, multiline_mark)
            if self.check:
                if len(CaseMetaChecker().check(meta)) > 0:
                    if self.verbose:
                        sys.stdout.write(' er\n')
                    return
        except (MetaParseError, NotSupportScriptError) as e:
            if self.verbose:
                sys.stdout.write('{} er\n'.format(e))
            return

        try:
            self.storage.store(meta)
        except UnicodeDecodeError as e:
            if self.verbose:
                sys.stdout.write('{} er\n'.format(e))
            return
        if self.verbose:
            sys.stdout.write(' ok\n')

    def export(self):
        def yat_handler(path, is_dir):
            if is_dir and is_yat_suite(path):
                for root, dirs, files in os.walk(os.path.join(path, 'testcase')):
                    for script in files:
                        if script_valid(script):
                            self._store(os.path.join(root, script))

        def normal_handler(path, is_dir):
            if not is_dir and script_valid(path):
                self._store(path)
        try:
            walk_path(self.src, yat_handler if self.yat else normal_handler)
        finally:
            self.storage.finish()
