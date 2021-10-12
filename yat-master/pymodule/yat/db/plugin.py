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

__db_mapper = { }


def get_db(user, password, host, port, driver: str = 'zenith', **kwargs):
    if driver not in __db_mapper:
        raise RuntimeError("found not support database type {}".format(driver))
    return __db_mapper[driver](user, password, host, port, **kwargs)


def db_plugin(name):
    def _wrapper(cls):
        if name in __db_mapper:
            raise RuntimeError("found duplicate database plugin with name = %s"  % name)
        __db_mapper[name] = cls

        return cls

    return _wrapper
