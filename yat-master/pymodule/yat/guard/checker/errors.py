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

class CheckErrorLevel:
    LEVEL_INFO = 3
    LEVEL_WARN = 4
    LEVEL_ERROR = 5

    __name_map = {
        LEVEL_INFO: 'INFO',
        LEVEL_WARN: 'WARN',
        LEVEL_ERROR: 'ERROR'
    }

    def __init__(self, level):
        self.level = level

    def __le__(self, other):
        return self.level <= other.level

    def __ge__(self, other):
        return self.level >= other.level

    def __lt__(self, other):
        return self.level < other.level

    def __gt__(self, other):
        return self.level > other.level

    def __eq__(self, other):
        return self.level == other.level

    def __repr__(self):
        return self.__name_map[self.level]


LEVEL_INFO = CheckErrorLevel(CheckErrorLevel.LEVEL_INFO)
LEVEL_WARN = CheckErrorLevel(CheckErrorLevel.LEVEL_WARN)
LEVEL_ERROR = CheckErrorLevel(CheckErrorLevel.LEVEL_ERROR)


class CheckErrorCode:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class CheckError:
    CHECK_ERROR = CheckErrorCode("CHECK_ERROR")
    CHECK_WARNING = CheckErrorCode("CHECK_WARNING")
    PARSE_ERROR = CheckErrorCode("PARSE_ERROR")
    PARSE_WARNING = CheckErrorCode("PARSE_WARNING")
    FILE_ERROR = CheckErrorCode("FILE_ERROR")

    def __init__(self, level: CheckErrorLevel, code: CheckErrorCode, name: str, err_type: str, msg: str, script: str):
        self.level = level
        self.code = code
        self.name = name
        self.type = err_type
        self.msg = msg
        self.script = script

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{}|{}|{}|{}|{}|{}".format(self.level, self.code, self.name, self.type, self.msg, self.script)

    def to_dict(self):
        return {
            "level": str(self.level),
            "code": str(self.code),
            "name": self.name,
            "type": self.type,
            "message": self.msg,
            "script": self.script
        }

    @staticmethod
    def error(code: CheckErrorCode, name: str, err_type: str, msg: str, script: str):
        return CheckError(LEVEL_ERROR, code, name, err_type, msg, script)

    @staticmethod
    def warning(code: CheckErrorCode, name: str, err_type: str, msg: str, script: str):
        return CheckError(LEVEL_WARN, code, name, err_type, msg, script)

    @staticmethod
    def info(code: CheckErrorCode, name: str, err_type: str, msg: str, script: str):
        return CheckError(LEVEL_INFO, code, name, err_type, msg, script)
