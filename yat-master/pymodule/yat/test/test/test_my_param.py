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
from yat.test.permutation import perm_param, param_case

_perm_case = (
    ('Y', 'N'),  # exp IGNORE option
    ('Y', 'N'),  # exp CREATE_USER option
    ('ALL', 'META_DATA_ONLY', 'DATA_ONLY'),  # exp CONTENT option
    (0, 1, 2, 32, 33),  # exp PARALLEL option
    ('TXT', 'BIN'),  # exp FILETYPE option

)


@param_case()
class TestExpPermutation(TestCase):
    """
    test exp with permuted options
    """
    node = Node()

    @classmethod
    def setUpClass(cls) -> None:
        """
        setup to create table and init data
        """
        cls.node.sql('create table test_1(id int primary key, name varchar(20))').success()
        for i in range(1000):
            cls.node.sql('insert into test_1 values(%d, dbe_random.get_string(20))', i)

    @perm_param(*_perm_case)
    def test_exp_one_table(self, parameter):
        """
        test export on table with permuted options
        """
        ignore, create_user, content, parallel, file_type = parameter
        self.node.exp(
            file='temp/exp.exp',
            tables='test_1',
            ignore=ignore,
            create_user=create_user,
            content=content,
            parallel=parallel,
            file_type=file_type
        ).contains('Logic Export Success')

    @classmethod
    def tearDownClass(cls) -> None:
        """
        cleanup test data
        """
        cls.node.sql('drop table test_1').success()
