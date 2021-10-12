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
from yat.test import Node


class TestNormal(unittest.TestCase):
    def test_normal_001(self):
        with Node() as node:
            node.sql('drop table if exists abc')
            node.sql("create table abc(id int)")

            node.sql('insert into abc values(1), (2), (3)')
            node.sql('commit')
            node.sh('zctl.py -t kill; zctl.py -t start')
            node.reset()
            node.sql('select * from abc')

    def test_normal_002(self):
        with Node(node='primary') as primary, Node(node='standby') as standby:
            primary.sql('drop table if exists abc')
            primary.sql("create table abc(id int)")

            primary.sql('insert into abc values(1), (2), (3)')
            primary.sql('commit')
            standby.sh('zctl.py -t kill; zctl.py -t start')
            standby.reset()
            standby.sql('select * from abc')
