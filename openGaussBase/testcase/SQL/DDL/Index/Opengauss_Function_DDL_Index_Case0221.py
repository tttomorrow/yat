"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
'''
Case Type： 功能
Case Name： 使用concurrently创建索引失败，遗留非法索引
Descption:
1.创建表，并插入数据
2.插入数据，使部分数据重复
3.创建唯一在线索引
4.查询索引
5.删除重复数据
6.索引重建
7.查询索引
'''
import unittest
from yat.test import Node
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

class Concurrently(unittest.TestCase):
    primary_sh = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.dbPrimaryDbUser = Node(node='PrimaryDbUser')
        self.log = Logger()
        self.Constant = Constant()
        self.tblname = 'ddl_index_case0221'
        self.idxname = 'ddl_index_case0221_idx'
        self.log.info('-----------------Opengauss_Function_DDL_Index_Case0221.py start----------------')

    def test_in_select(self):
        self.log.info('-------------------create table--------------------------------')
        result = self.primary_sh.execut_db_sql(
            f'DROP TABLE IF EXISTS {self.tblname};CREATE TABLE {self.tblname}(id INT, first_name text, last_name text);')
        self.log.info(result)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, result)
        self.log.info('-------------------insert data--------------------------------')
        result = self.primary_sh.execut_db_sql(f'INSERT INTO {self.tblname} SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,2000000) AS id) AS x;')
        self.log.info(result)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, result)

        self.log.info('-------------------insert data repetition--------------------------------')
        result = self.primary_sh.execut_db_sql(
            f'INSERT INTO {self.tblname} SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,20) AS id) AS x;')
        self.log.info(result)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, result)

        self.log.info('-----------------create index fail-----------------------------')
        sql = f'create unique index concurrently {self.idxname} on {self.tblname}(id);'
        result = self.primary_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('could not create unique index', result)
        self.assertIn('duplicated', result)

        self.log.info('-----------------show index -----------------------------')
        sql = f'\\d {self.tblname};'
        result = self.primary_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('INVALID', result)

        self.log.info('-----------------delete repeating data-----------------------------')
        sql = f'delete from {self.tblname} where id<21;'
        result = self.primary_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.Constant.DELETE_SUCCESS_MSG, result)

        self.log.info('-----------------reindex data-----------------------------')
        sql = f'reindex index {self.idxname};'
        result = self.primary_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.Constant.REINDEX_SUCCESS_MSG, result)

        self.log.info('-----------------show index -----------------------------')
        sql = f'\\d {self.tblname};'
        result = self.primary_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn('INVALID', result)

    def tearDown(self):
        self.log.info('----------------this is tearDown------------------------------------')
        self.log.info('----------------drop table------------------------------------')
        result = self.primary_sh.execut_db_sql(f'drop table if exists {self.tblname};')
        self.log.info(result)
