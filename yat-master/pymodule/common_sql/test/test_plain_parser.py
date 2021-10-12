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
from common_sql.plain_parser import PlainParser


class TestPlainParser(unittest.TestCase):
    def test_parser(self):
        parser = PlainParser('''------------------------------------------------------------------------------------------------------
| Id  | Description                          | Owner | Name           | Rows | Cost | Bytes | Remark |
------------------------------------------------------------------------------------------------------
| 0   | SELECT STATEMENT                     |       |                |      |      |       |        |
| 1   |   VIEW                               | YAT   | ADM_TABLES     |      |      |       |        |
| 2   |     HASH JOIN(L)                     |       |                |      |      |       |        |
| 3   |       NESTED LOOPS                   |       |                |      |      |       |        |
| 4   |         TABLE ACCESS FULL            | SYS   | SYS_USERS      |      |      |       |        |
| 5   |         TABLE ACCESS BY INDEX ROWID  | SYS   | SYS_TABLES     |      |      |       |        |
| 6   |           INDEX UNIQUE SCAN          | SYS   | IX_TABLE$001   |      |      |       |        |
| 7   |       TABLE ACCESS FULL              | SYS   | DV_TABLESPACES |      |      |       |        |
------------------------------------------------------------------------------------------------------
Predicate Information (identified by id):
-----------------------------------------
   2 - access: T.SPACE# = TS.ID
   5 - filter: T.RECYCLED = 0
   6 - access: T.USER# = U.ID''')

        tree = parser.parse()

        self.assertEqual(tree.tree.name, 'root')
        self.assertEqual(tree.tree.left.name, 'SELECT STATEMENT')
        self.assertEqual(tree.tree.left.left.left.name, 'HASH JOIN(L)')
