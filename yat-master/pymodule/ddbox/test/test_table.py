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

import ddbox
from yat.test.node import Node


class TestDdBox(unittest.TestCase):
    class TestAbc(unittest.TestCase):
        node = Node()

        @classmethod
        def setUp(cls):
            ddbox.add_template(
                't1',
                ('col1', 'char'),
                ('col2', 'char'),
                ('col3', 'char'),
                ('col4', 'char'),
                ('col5', 'char')
            )

            ddbox.add_template_random(
                't2',
                data_types=(
                    'char(20)',
                    'int',
                    'bigint',
                    'clob',
                    'blob',
                    'binary',
                    'varchar(100)'
                ),
                column_count=30,
            )

        def test_001(self):
            ddbox.table('tbl1', template='t1').rows(10000).create(self.node)
            self.node.sql(ddbox.table('tbl1', template='t1').rows(10000).text())

            self.node.sqls(ddbox.table('tbl2', template='t1').rows(10000).index(
                'unique', ('col1', 'col2')
            ).text())
            
