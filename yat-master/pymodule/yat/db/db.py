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

from abc import ABC


class DBTransaction:
    def __init__(self, db):
        self._db = db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self._db.commit()
        else:
            self._db.rollback()


class DB(ABC):
    """
    The database client base class, and all the implement must extend this class
    """
    def __init__(self, user, password, host, port, **kwargs):
        self.db = None
        self.db_error = None
        self.connection = None
        self.cursor = None
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    @property
    def autocommit(self):
        """
        get the connection is autocommit or not
        """
        return self.connection.autocommit

    @autocommit.setter
    def autocommit(self, value):
        """
        set the connection to autocommit or not
        """
        self.connection.autocommit = value

    def execute(self, sql, *args):
        """
        execute given sql with arguments
        :param sql: sql to execute
        :param args: argument bind to the sql
        """
        self.cursor.execute(sql, args)

    def fetch_all(self):
        """
        get all the result set
        """
        return self.cursor.fetchall()

    def execute_query(self, sql, *args):
        """
        execute given sql with arguments and return all the result
        :param sql: sql to execute
        :param args: args bing to the sql
        :return: result set
        """
        self.execute(sql, *args)
        return self.fetch_all()

    def close(self):
        """
        close this database connection
        """
        self.cursor.close()
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def transaction(self):
        return DBTransaction(self)
