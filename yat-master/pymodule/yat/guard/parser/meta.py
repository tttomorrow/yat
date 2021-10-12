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
#the test case's meta data


class DTS:
    def __init__(self, dts, fixer=None):
        self.dts = dts
        self.fixer = fixer

    def __str__(self):
        return "{{ DTS: {}, fixer: {} }}".format(self.dts, self.fixer)

    def __repr__(self):
        return self.__str__()


class CaseMeta(dict):
    """
    the test's meta data instance, any attribute can be save to this object,
    and it is read only
    """
    def __init__(self, script):
        super(CaseMeta, self).__init__()
        self['script'] = script

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value

    def __str__(self):
        truncate = ["{\n"]
        for name in self.__dict__:
            value = self.__dict__[name]
            truncate.append('\t{}: {}\n'.format(name, value))

        truncate.append("}")
        return "".join(truncate)

    def __repr__(self):
        return self.__str__()
