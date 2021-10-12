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

from types import GeneratorType

from ..db import DB
from ..plugin import db_plugin

# the system is good when no using the driver
_driver_exists = True

try:
    import pyzenith
except ImportError:
    _driver_exists = False


ZENITH_DEFAULT_TIMEOUT = 600


def _args_filter(args):
    """
    zenith db api only accept list of tuple arguments for bind execute, that is ungainly
    so we should make all kind of arguments to list of tuple arguments
    """
    if isinstance(args, (GeneratorType, )):
        args = list(args)

    if len(args) <= 0:
        return []

    if isinstance(args[0], (tuple, list,)):
        return [tuple(v) for v in args]
    else:
        return [tuple(args), ]


@db_plugin('zenith')
class ZenithDB(DB):
    """
    zenith database implement of database client
    """
    def __init__(self, user, password, host, port, **kwargs):
        global _driver_exists
        super(ZenithDB, self).__init__(user, password, host, port, **kwargs)

        if not _driver_exists:
            raise RuntimeError("zenith driver is no exists, place make sure that you initial it correctly")

        timeout = kwargs.get('timeout', ZENITH_DEFAULT_TIMEOUT)

        self.db = pyzenith
        self.db_error = pyzenith.DatabaseError
        self.connection = self.db.connect(user=user, passwd=password, host=host, port=port, sockettimeout=timeout)
        self.cursor = self.connection.cursor()

    def execute(self, sql, *args):
        if len(args) > 0:
            self.cursor.execute_ex(sql, _args_filter(args))
        else:
            self.cursor.execute_ex(sql)

    def fetch_all(self):
        return self.cursor.fetchall_ex()
