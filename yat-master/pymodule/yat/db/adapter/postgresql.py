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

from ..db import DB
from ..plugin import db_plugin

# the system is good when no using the driver
_driver_exists = True

try:
    import psycopg2
except ImportError:
    _driver_exists = False

_DEFAULT_TIMEOUT = 600


@db_plugin('postgresql')
class PostgresqlDB(DB):
    """
    postgresql database implement of database client
    """

    def __init__(self, user, password, host, port, **kwargs):
        global _driver_exists
        super(PostgresqlDB, self).__init__(user, password, host, port, **kwargs)

        if not _driver_exists:
            raise RuntimeError("postgresql driver is no exists, place make sure that you initial it correctly")

        dbname = kwargs['dbname']

        self.db = psycopg2
        self.db_error = psycopg2.Error
        self.connection = self.db.connect(user=user, password=password, host=host, port=port, dbname=dbname)
        self.cursor = self.connection.cursor()

