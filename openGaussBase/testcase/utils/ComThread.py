"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
import threading
from threading import *


# 重写线程类，以获取返回值
class ComThread(Thread):
    def __init__(self, func, args):
        super(ComThread, self).__init__()
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        return self.result


# 重写定时器类，以获取返回值
class ComTimer(Timer):
    def __init__(self, interval, function, args, kwargs):
        self.func = function
        super(ComTimer, self).__init__(interval, self.func)
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.result = self.function(*self.args, **self.kwargs)
        self.finished.set()

    def get_result(self):
        return self.result


# 重写线程类，以上锁
class ComThreadWithLock(Thread):
    def __init__(self, func, args):
        super(ComThreadWithLock, self).__init__()
        self.func = func
        self.args = args
        self.result = None
        self.lock = threading.Lock()

    def run(self):
        with self.lock:
            self.result = self.func(*self.args)

    def get_result(self):
        return self.result
