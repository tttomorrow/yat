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

import unittest
import paramunittest


@paramunittest.parametrized (
    ("abc", ),
    ("bbc", ),
    ("xxx", ),
    ("bbx", ),
    ("yyy", ),
    ("gcc", )
)
class TestStats(unittest.TestCase):
    def __init__(self, method='runTest'):
        super().__init__(method)
        self.param = None

    def setParameters(self, param):
        self.param = param

    def test_stats(self):
        if self.param == 'abc':
            self.assertTrue(False)


class StandTestCase(unittest.TestCase):
    conn = None
    cursor = None

    @classmethod
    def setUpClass(cls):
        cls.conn = pyzenith.connect(user='user', passwd='pass', host='host', port='port')
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        if cls.conn:
            cls.conn.close()

    def test_stand_001(self):
        self.cursor.execute('select count(1) from dv_sessiones')
        res = self.cursor.fetchall()
        self.assertTrue(len(res) == 1)
        self.assertTrue(res[0][0] > 0)

    def test_stand_002(self):
        self.cursor.execute('create table abc(id int)')
        self.cursor.execute('insert into abc values(1), (2), (3)')
        self.cursor.execute('select * from abc')
        res = self.cursor.fetchall()
        self.assertEqual(len(res), 3)
        self.assertListEqual(res[0], [1, ])
        self.assertListEqual(res[1], [2, ])
        self.assertListEqual(res[2], [3, ])

