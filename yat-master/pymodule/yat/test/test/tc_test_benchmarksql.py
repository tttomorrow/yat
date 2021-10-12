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

from yat.test import BenchmarkSql
from yat.test import Node


common_script = (
    'drop table if exists abc',
    '''
    create table abc (
        id int,
        name varchar(20),
        address varchar(1024)
    )
    ''',
    '''
    declare
        i int := 1;
    begin
        -- do with i
    end;
    '''
)


class TestBenchmark(unittest.TestCase):
    node = Node()
    bench = BenchmarkSql(
        'data/benchmarksql-5.0',
        'temp/benchmarksql',
        conn='jdbc:zenith:@127.0.0.1:9797',
        user='sys',
        password=''
    )

    @classmethod
    def setUpClass(cls):
        cls.bench.destroy()
        cls.bench.build()

    def test_bench_001(self):
        self.bench.run()  # wait the benchmark finished

    def test_bench_002(self):
        self.bench.run(20)  # wait 20 seconds, when ever the benchmark is finished or not

    def test_bench_003(self):
        proc = self.bench.run_background()  # run in background

        # do other thing
        try:
            for i in range(30):
                self.node.sql('select * from dv_sessiones')
        except Exception as e:
            raise e
        finally:
            proc.kill()  # kill benchmark

    def test_bench_004(self):
        proc = self.bench.run_background()  # run in background

        # do other thing
        for i in range(30):
            self.node.sql('select * from dv_sessiones')

        proc.wait(30)  # wait benchmark to finished, more than 30 seconds
