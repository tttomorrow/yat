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

__node_plugins = {}


def get_plugins(db_type):
    if db_type not in __node_plugins:
        return {}
    return __node_plugins[db_type]


def plugin(db_type, name=None):
    """
    decorator to register node plugin methods
    """
    def _wrapper(fun):
        real_name = name
        if real_name is None:
            real_name = fun.__name__

        db_plugins = __node_plugins.get(db_type)

        if db_plugins is None:
            __node_plugins[db_type] = {real_name: fun}
        else:
            db_plugins[real_name] = fun
        return fun

    return _wrapper
