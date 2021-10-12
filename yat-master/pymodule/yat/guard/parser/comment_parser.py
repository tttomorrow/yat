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

from collections import deque
from io import IOBase
from io import StringIO

from .errors import EndError


class CommentParser:
    """
    Parse stream to 
    """
    def __init__(self, script, line_mark, multiline_mark):
        if isinstance(script, IOBase):
            self.stream = script
        else:
            self.stream = StringIO(script)

        self.line_marks = line_mark
        self.multiline_marks = multiline_mark
        self.queue_max_len = self._get_max_len()
        self.mark_queue = deque()

    def _get_max_len(self):
        max_l = 0
        max_m = 0
        if self.line_marks:
            max_l = max((len(it) for it in self.line_marks))
        if self.multiline_marks:
            max_m = max(max(len(it[0]), len(it[1]),) for it in self.multiline_marks)

        if max_l + max_m == 0:
            raise RuntimeError("line or multiline comment mark should be supply")
        return max(max_l, max_m)

    def parse(self):
        lines = []
        try:
            self.init_queue()

            while True:
                queue_val = ''.join(self.mark_queue)
                found = False
                if self.line_marks:
                    for line_mark in self.line_marks:
                        if queue_val.startswith(line_mark):
                            prefix = None
                            if len(line_mark) < len(queue_val):
                                prefix = queue_val[len(line_mark):]
                            lines.append(self.read_until('\n', prefix))
                            self.init_queue()
                            found = True

                if found:
                    continue
                if self.multiline_marks:
                    for start, end in self.multiline_marks:
                        if queue_val.startswith(start):
                            prefix = None
                            if len(start) < len(queue_val):
                                prefix = queue_val[len(start):]
                            lines.append(self.read_until(end, prefix))
                            self.init_queue()
                            found = True

                if not found:
                    self.move_queue()
        except EndError:
            pass

        return '\n'.join(lines)

    def read(self, n=1):
        ch = self.stream.read(n)
        if len(ch) == 0:
            raise EndError()
        return ch

    def read_until(self, until, prefix=None):
        if prefix is None:
            prefix = deque()
        else:
            prefix = deque(prefix)

        queue = deque()

        def _read():
            if len(prefix) > 0:
                return prefix.popleft()
            else:
                return self.read()
        [queue.append(_read()) for _ in range(len(until))]
        res = []
        while True:
            queue_val = ''.join(queue)
            if queue_val == until:
                return ''.join(res)
            else:
                res.append(queue.popleft())
                queue.append(_read())

    def readline(self):
        line = self.stream.readline()
        if len(line) == 0:
            raise EndError()

        return line.strip('\r\n')

    def init_queue(self):
        seqs = [ch for ch in self.read(self.queue_max_len)]

        self.mark_queue.clear()
        [self.mark_queue.append(it) for it in seqs]

    def move_queue(self):
        ch = self.read()
        self.mark_queue.popleft()
        self.mark_queue.append(ch)
