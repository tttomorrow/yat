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

import re
from datetime import datetime

from yat.guard.report.basic import Reporter
from yat.guard.report.report_manager import reporter

_init_sqls = (
    'drop table if exists gd_check_error',
    '''
    create table gd_check_error
    (
        err_time datetime,
        err_level char(8),
        err_code varchar(16),
        err_checker_name varchar(64),
        err_type varchar(128),
        err_msg varchar(1024),
        err_case_path varchar(1024)
    )
    '''
)

_check_sql = "select count(1) from user_tables where table_name ='GD_CHECK_ERROR'"

_insert_sql = """
    insert into gd_check_error
    (
        err_time,
        err_level, 
        err_code, 
        err_checker_name, 
        err_type,
        err_msg, 
        err_case_path
    )
    values (?, ?, ?, ?, ?, ?, ?)
"""


@reporter
class ZenithReport(Reporter):
    def __init__(self, url, **opts):
        self._cache = []
        self._batch_size = opts.get('batch_size', 200)

        user, password, host, port = self._parse_url(url)
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.pyzenith = __import__('pyzenith')
        self.connect = self.pyzenith.connect(user=self.user, passwd=self.password, host=self.host, port=self.port)
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)
        self.opts = opts

        if not self._check_db():
            self._init_db()

    _url_pattern = re.compile(
        r'^db:zenith:([a-zA-Z0-9_]+)/'
        r'([a-zA-Z0-9@_.#$%^&*]+)@'
        r'([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}|'
        r'(?:[a-zA-Z0-9_-]+.)*(?:[a-zA-Z0-9_-]+))'
        r'(?::([0-9]+))?$'
    )

    def _init_db(self):
        for sql in _init_sqls:
            self._execute(sql)
        self.connect.commit()

    def _execute(self, sql):
        self.cursor.execute(sql)

    def _select(self, sql, *params):
        self._select_inner(sql, *params)

        return self.cursor.fetchall()

    def _select_one(self, sql, *params):
        self._select_inner(sql, *params)

        return self.cursor.fetchone()

    def _select_inner(self, sql, *params):
        if len(params) > 0:
            args = [tuple([str(it) for it in params])]
            self.cursor.execute(sql, args)
        else:
            self.cursor.execute(sql)

    def _insert(self, sql, *params):
        args = [str(it) for it in params]
        self.cursor.execute(sql, [tuple(args)])

    def _batch_insert(self, sql, *params):
        args = []
        for param in params:
            args.append(tuple([str(it) for it in param]))

        self.cursor.execute(sql, args)
        self.connect.commit()

    def _check_db(self):
        return self._select(_check_sql)[0] == 1

    def report(self, error):
        self._cache.append(error)
        if len(self._cache) > self._batch_size:
            self._flush()

    def _flush(self):
        params = []
        for error in self._cache:
            params.append((
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                error.level, error.code, error.name, error.type, error.msg, error.script
            ))

        try:
            self._batch_insert(_insert_sql, *params)
        except self.pyzenith.DatabaseError as e:
            print('check store with error: %s' % str(e))
        finally:
            self._cache = []

    def finish(self):
        self._flush()
        self.connect.close()

    def _parse_url(self, url):
        matcher = self._url_pattern.match(url)
        return matcher.group(1), matcher.group(2), matcher.group(3), matcher.group(4)

    @classmethod
    def match(cls, url):
        return None is not cls._url_pattern.match(url)
