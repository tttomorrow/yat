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


class PlainReader:
    def __init__(self, content):
        if isinstance(content, (str, )):
            self.content = content.splitlines(keepends=False)
        else:
            self.content = content

        self.content_iter = iter(self.content)
        self._cache = None

    def next_line(self):
        if self._cache is None:
            return next(self.content_iter)
        else:
            swap = self._cache
            self._cache = None
            return swap

    def top_line(self):
        if self._cache is None:
            self._cache = next(self.content_iter)

        return self._cache

    def skip_line(self):
        if self._cache is None:
            next(self.content_iter)
        else:
            self._cache = None

    def has_next(self):
        try:
            if self._cache is None:
                self._cache = next(self.content_iter)
            return True
        except StopIteration:
            return False
