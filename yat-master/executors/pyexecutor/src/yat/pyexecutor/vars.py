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
from threading import RLock


class Vars:
    def __init__(self):
        self.__dict__['_lock'] = RLock()
        self.__dict__['_vars'] = {}

    def __getattr__(self, item):
        return self._get_safe(item)

    def __setattr__(self, key, value):
        self._set_safe(key, value)

    def __getitem__(self, item):
        return self._get_safe(item)

    def __setitem__(self, key, value):
        self._set_safe(key, value)

    def __delitem__(self, key):
        self._del_safe(key)

    def __delattr__(self, item):
        self._del_safe(item)

    def clear(self):
        self._lock.acquire(True)
        try:
            self._vars.clear()
        finally:
            self._lock.release()

    def items(self):
        self._lock.acquire(True)
        try:
            return self._vars.items()
        finally:
            self._lock.release()

    def _get_safe(self, item):
        self._lock.acquire(True)
        try:
            return self._vars[item]
        finally:
            self._lock.release()

    def _set_safe(self, item, value):
        self._lock.acquire(True)
        try:
            self._vars[item] = value
        finally:
            self._lock.release()

    def _del_safe(self, key):
        self._lock.acquire(True)
        try:
            del self._vars[key]
        finally:
            self._lock.release()


var = Vars()
