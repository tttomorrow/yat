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


class PathSearch:
    def __init__(self, *paths):
        self.paths = list(paths)

    def add_search_path(self, path):
        self.paths.append(path)

    def search(self, *names):
        for name in names:
            if os.path.isabs(name):
                if os.path.exists(name):
                    return name
                else:
                    return None
            for path in self.paths:
                real_path = os.path.join(path, name)
                if os.path.exists(real_path):
                    return real_path

        return None

