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

_dts_pattern = re.compile(r'^DTS[0-9]{8}(?:[0-9]{5}|[0-9a-zA-Z]{11})$')
_employee_pattern = re.compile(r'^[a-z](?:wx)?[0-9]{6,10}$')


class Context:
    def __init__(self):
        # comment settings
        self.valid_case = {
            '.py': (
                ('#',), (("'''", "'''"), ('"""', '"""'))
            ),
            '.sql': (
                ('--', ), (('/*', '*/'), )
            ),
            '.sh': (
                ('#', ), None
            ),
            '.go': (
                ('//', ), (('/*', '*/'), )
            ),
            '.java': (
                ('//', ), (('/*', '*/'), )
            ),
            '.groovy': (
                ('//', ), (('/*', '*/'), ('"""', '"""'), ("'''", "'''"))
            ),
            '.c': (
                ('//',), (('/*', '*/'),)
            ),
            '.cc': (
                ('//',), (('/*', '*/'),)
            ),
            '.cpp': (
                ('//',), (('/*', '*/'),)
            ),
            '.cxx': (
                ('//',), (('/*', '*/'),)
            ),
            '.h': (
                ('//',), (('/*', '*/'),)
            )
        }

        self.second_ext = ('.iz', '.z', '.r', '.unit', '.p')

        self.checkers = None

        # meta check settings
        self.meta_checker = {
            'owner': {
                'required': True,
                'checker': re.compile(_employee_pattern)
            },
            'requirement': {
                'required': True,
                'checker': (
                    re.compile(r'^ST[0-9]{4}-[0-9]{1,3}$'),
                    re.compile(r'^SR\.IREQ[0-9]{8}\.[0-9]{3}$'),
                    re.compile(r'^AR\.SR\.IREQ[0-9]{8}\.[0-9]{3}\.[0-9]{3}$'),
                    re.compile(_dts_pattern),
                    re.compile(r'^Unknown$')
                )
            },
            'date': {
                'required': True,
                'checker': None
            },
            'describe': {
                'required': True,
                'checker': None
            },
            'developer': {
                'required': True,
                'checker': (
                    re.compile(_employee_pattern),
                    re.compile(r'^Unknown$')
                )
            },
            'testpoint': {
                'required': False,
                'checker': None
            },
            'dts': {
                'required': False,
                'checker': re.compile(_dts_pattern)
            }
        }

        # charset settings
        self.valid_charset = ['utf-8', 'gbk']

        # test case checker setting
        self.case_name_checker = {
            'name_regex': re.compile(r'^tc(?:_[a-z][0-9a-z]{1,9}){1,6}(?:_[0-9]{1,4})$'),
            'feature_regex': re.compile(r'[a-z][0-9a-z]{1,9}'),
            'serial_regex': re.compile(r'[0-9]{1,4}'),
            'serial_max_size': 4,
            'feature_max_count': 6,
            'feature_size': [2, 10],
            'prefix': 'tc',
            'weak_name_regex': re.compile(r'^[0-9a-zA-Z]{1,20}(?:[-_][0-9a-zA-Z]{1,20}){0,8}$')
        }

        self.case_size_checker = {
            'max_line': 3000,
            'max_size': 100000
        }


ctx = Context()
