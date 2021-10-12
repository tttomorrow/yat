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


class MyTestCase(unittest.TestCase):
    node = Node()

    backup_invalid_opts = [
        '--backup-key',
        '--xxx',
        '--show'
    ]

    def test_backup_not_support(self):
        roach_cmd = 'python3 $ROACH_HOME/GaussRoach.py -t backup {}';
        for invalid_opt in self.backup_invalid_opts:
            self.node.sh(roach_cmd.format(invalid_opt)).not_code(0)
