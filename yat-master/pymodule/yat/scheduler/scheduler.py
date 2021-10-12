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
import re
import stat
from subprocess import Popen
from threading import Thread, Lock

from .parser import BlockNode, ActionNode
from .parser import Parser

PATH_REGEX = re.compile(r'^/?([a-zA-Z0-9._-]+/)*[a-zA-Z0-9._-]+$')


class Counter:
    def __init__(self, value=0):
        self._value = value
        self.lock = Lock()

    def inc_and_get(self):
        with self.lock:
            self._value += 1
            return self._value

    def get_and_inc(self):
        with self.lock:
            v = self._value
            self._value += 1
            return v

    @property
    def value(self):
        with self.lock:
            return self._value


class Scheduler:
    def __init__(self, **kwargs):
        if 'path' in kwargs:
            path = os.path.abspath(kwargs['path'])
            with open(path, 'r') as fstream:
                self.stream = Parser(fstream).parse()
            work_dir = os.path.dirname(path)
        else:
            self.stream = Parser(kwargs['stream']).parse()
            work_dir = '.'

        self.work_dir = os.path.abspath(kwargs.get('work_dir', work_dir))

        self.log_dir = kwargs.get('log_dir', None)
        self.width = kwargs['width'] if 'width' in kwargs else 100
        self.color = kwargs['color'] if 'color' in kwargs else False
        self.counter = Counter()

    def schedule(self):
        if self.log_dir and not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        self.schedule_block(self.stream)

    def schedule_block(self, block):
        if block.name == 'parallel':
            self.schedule_parallel(block.sub_blocks)
        elif block.name == 'serial':
            self.schedule_serial(block.sub_blocks)
        else:
            raise RuntimeError('unknown block found with name %s' % block.name)

    def schedule_parallel(self, blocks):
        threads = []

        for block in blocks:
            if isinstance(block, ActionNode):
                thread = Thread(target=lambda v: self.schedule_action(v), args=(block,))
                thread.start()
                threads.append(thread)
            elif isinstance(block, BlockNode):
                thread = Thread(target=lambda v: self.schedule_block(v), args=(block,))
                thread.start()
                threads.append(thread)
            else:
                raise RuntimeError('unknown block found %s' % block)

        [thread.join() for thread in threads]

    def schedule_serial(self, blocks):
        for block in blocks:
            if isinstance(block, ActionNode):
                self.schedule_action(block)
            elif isinstance(block, BlockNode):
                self.schedule_block(block)
            else:
                raise RuntimeError('unknown block found %s' % block)

    def schedule_action(self, action):
        if action.name == 'run':
            self.schedule_run_action(action)
        elif action.name == 'suite':
            self.schedule_suite_action(action)
        else:
            raise RuntimeError('unknown action name %s found' % action.name)

    def schedule_run_action(self, action):
        self._shell_action(action.params)

    def schedule_suite_action(self, action):
        if len(action.params) < 1:
            raise RuntimeError('suite action require at last one param')
        suite = action.params[0]

        if not PATH_REGEX.match(suite):
            raise RuntimeError('suite action given a invalid path: ' % action.content)

        if os.path.isabs(suite):
            suite_dir = suite
        else:
            suite_dir = os.path.join(self.work_dir, suite)

        shell_arry = ["yat" , "suite" , "run" , "--bare"]
        if self.color:
            shell_arry.append(self.color)

        shell_arry.append("--width")
        shell_arry.append(self.width)
        shell_arry.append("-d")
        shell_arry.append(suite_dir)
        shell_arry.append(' '.join(action.params[1:]))
        self._shell_action(shell_arry)

    def _shell_action(self, cmd):
        if self.log_dir:
            count = self.counter.get_and_inc()
            output_name = os.path.join(self.log_dir, '.%d.log' % count)
            flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
            mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
            with os.fdopen(os.open(output_name, flags, mode), 'w') as out:
                Popen(cmd, stderr=out, stdout=out).wait()
        else:
            Popen(cmd).wait()
