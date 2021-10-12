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

from unittest import TestCase

from yat.test import Node


class TestPrimaryStandby(TestCase):
    node = None
    node_standby = None

    test_table_drop = 'drop table if exists tbl_test';
    test_table_create = '''create table tbl_test (
        id int,
        name char(20),
        address varchar(1024)
    )
    '''

    @classmethod
    def make_data(cls):
        values = []
        for i in range(10):
            values.append((i, 'xxx', 'xxxxxxxxxxxxxxxxxxx',))

        cls.node.sql('insert into tbl_test values (?, ?, ?)', *values)

    @classmethod
    def setUpClass(cls):
        cls.node = Node(node='primary')
        cls.node_standby = Node(node='standby')
        cls.node.sql(cls.test_table_drop)
        cls.node.sql(cls.test_table_create)
        cls.make_data()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.node.close()

    def test_abc_001(self):
        self.node.sh('echo "success"').expect('success')

        self.node.sql('select * from tbl_test').expect(
            (1, 'xxx                 ', 'xxxxxxxxxxxxxxxxxxx'),
            (2, 'xxx                 ', 'xxxxxxxxxxxxxxxxxxx'))

    def test_abc_standby(self):
        sql = 'select * from tbl_test limit 5'
        self.node.sql(sql).result()
        self.node.sql(sql).result()

    def test_abc_002(self):
        self.node.sh('cm ctl query').contains('success')

    def test_abc_003(self):
        self.node.sh('cm ctl query').regex(r'.*success.*')

    def test_abc_004(self):
        self.node.sql('select * from tbl_test').ors(
            ('contains', (1, 'xxx                 ', 'xxxxxxxxxxxxxxxxxxx')),
            ('expect',
                (0, 3, 4),
                (3, 5, 7)),
            ('ands',
                ('contains', (2, 4, 5)),
                ('regex', '.*[0-9]')))

        self.node.sql('select * from tbl_test').ands(
            ('expect', ((0, 2, 4), (3, 5, 6))),
            ('expect', ((0, 6, 4), (3, 5, 7))),
            ('ands', (
                ('contains', (1, 4, 5)),
                ('regex', '.*[0-9]'))))

    def test_abc_005(self):
        with Node("node2") as node:
            node.sql("select * from tbl_test")
