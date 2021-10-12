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
# export meta data to zenith database

import hashlib
import os
import re

from yat.guard.export import storage

# sql to init database
_init_sql = (
    'drop table if exists gd_case',
    '''
    create table gd_case
    (
        c_id char(32) primary key,
        c_path varchar(512) not null,
        c_name varchar(64) not null,
        c_date date not null,
        c_describe varchar(2048)
    )
    ''',
    'drop table if exists gd_case_content',
    '''
    create table gd_case_content
    (
        c_id char(32) not null,
        c_content clob
    )
    ''',
    'drop table if exists gd_requirement',
    '''
    create table gd_requirement
    (
        c_id char(32),
        r_requirement varchar(32) not null
    )
    ''',
    'drop table if exists gd_test_point',
    '''
    create table gd_test_point
    (
        c_id char(32),
        p_test_point varchar(2048)
    )
    ''',
    'drop table if exists gd_dts',
    '''
    create table gd_dts
    (
        c_id char(32),
        d_dts char(16)
    )
    ''',
    'drop table if exists gd_owner',
    '''
    create table gd_owner
    (
        c_id char(32),
        o_id char(9)
    )
    '''
)

_check_db_sql = """
    select count(1) from user_tables where table_name in
    (
        'GD_CASE',
        'GD_DTS',
        'GD_OWNER',
        'GD_TEST_POINT',
        'GD_REQUIREMENT',
        'GD_CASE_CONTENT'
    )
"""


_insert_sql = {
    'case': 'insert into gd_case(c_id, c_name, c_path, c_date, c_describe) values (?, ?, ?, ?, ?)',
    'case_content': 'insert into gd_case_content(c_id, c_content) values (?, ?)',
    'dts': 'insert into gd_dts(c_id, d_dts) values (?, ?)',
    'testpoint': 'insert into gd_test_point(c_id, p_test_point) values (?, ?)',
    'requirement': 'insert into gd_requirement(c_id, r_requirement) values (?, ?)',
    'owner': 'insert into gd_owner(c_id, o_id) values(?, ?)'
}


@storage
class ZenithStorage:
    def __init__(self, url, **opts):
        user, password, host, port = self._parse_url(url)
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.pyzenith = __import__('pyzenith')
        self.connect = self.pyzenith.connect(user=self.user, passwd=self.password, host=self.host, port=self.port)
        self.cursor = self.connect.cursor()
        self.connect.autocommit(False)
        self.opts = opts

        append = opts.get('append', False)
        if append:
            if not self._check_db():
                self._init_db()
        else:
            self._init_db()

        self._cache = []
        self._batch_size = opts.get('batch_size', 200)

    _url_pattern = re.compile(r'^db:zenith:([a-zA-Z0-9_]+)/'
                              r'([a-zA-Z0-9@_.#$%^&*]+)@'
                              r'([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}|'
                              r'(?:[a-zA-Z0-9_-]+.)*(?:[a-zA-Z0-9_-]+))'
                              r'(?::([0-9]+))?$')

    def _parse_url(self, url):
        matcher = self._url_pattern.match(url)
        return matcher.group(1), matcher.group(2), matcher.group(3), matcher.group(4)

    @classmethod
    def match(cls, url):
        return None is not cls._url_pattern.match(url)

    def _check_db(self):
        self.cursor.execute(_check_db_sql)
        return self.cursor.fetchone()[0] == '6'

    def _init_db(self):
        for sql in _init_sql:
            self.cursor.execute(sql)
        self.connect.commit()

    def _insert(self, sql, *params):
        args = [str(it) for it in params]
        self.cursor.execute(sql, [tuple(args)])

    def store(self, meta):
        self._cache.append(meta)
        if len(self._cache) >= self._batch_size:
            self._flush()

    def _flush(self):
        try:
            for meta in self._cache:
                case_id = self._gen_case_id(meta.script)
                try:
                    self._insert(_insert_sql['case'], case_id, os.path.basename(meta.script), meta.script, meta.date, meta.describe)
                    self._insert(_insert_sql['case_content'], case_id, self._read_file(meta.script))

                    for dts in meta.dts:
                        self._insert(_insert_sql['dts'], case_id, dts.dts)
                    for testpoint in meta.test_points:
                        self._insert(_insert_sql['testpoint'], case_id, testpoint)
                    for sr in meta.requirement:
                        self._insert(_insert_sql['requirement'], case_id, sr)
                    for owner in meta.owner:
                        self._insert(_insert_sql['owner'], case_id, owner)
                except self.pyzenith.DatabaseError as e:
                    print('store %s failed: %s' % (meta.script, str(e)))
            self.connect.commit()
        finally:
            self._cache = []

    def _gen_case_id(self, script):
        with open(script, 'rb') as case:
            md5 = hashlib.md5()
            md5.update(case.read())
            md5.update(script)
            return md5.hexdigest()

    def _read_file(self, f):
        with open(f) as fin:
            return fin.read()

    def finish(self):
        self._flush()
        self.connect.close()
