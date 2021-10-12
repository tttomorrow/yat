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
"""
Case Type   : 功能
Case Name   : 对不同表并行创建concurrently索引
Description :
    1.创建表a，并插入数据
    2.创建表b，并插入数据
    3.同时创建concurrently索引
Expect      :
    1.创建表成功，插入数据成功
    2.创建表成功，插入数据成功
    3.创建索引成功
History     :
"""
import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.ComThread import ComThread


class Concurrently(unittest.TestCase):
    primary_sh = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.dbPrimaryDbUser = Node(node='PrimaryDbUser')
        self.log = Logger()
        self.Constant = Constant()
        self.tblname = 'ddl_index_case0234'
        self.tblname_no_rel = 'ddl_index_case0234_no_rel'
        self.idxname = 'ddl_index_case0234_idx'
        self.idxname_no_rel = 'ddl_index_case0234_no_rel_idx'
        self.log.info('------------------Opengauss_Function_DDL_Index_case0234.py start---------------------')

    def test_in_select(self):
        self.log.info('-------------------create table--------------------------------')
        result = self.primary_sh.execut_db_sql(
            f'DROP TABLE IF EXISTS {self.tblname};CREATE TABLE {self.tblname}(id INT, first_name text, last_name text);')
        self.log.info(result)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, result)
        self.log.info('-------------------insert data--------------------------------')
        result = self.primary_sh.execut_db_sql(f'INSERT INTO {self.tblname} SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,8000000) AS id) AS x;\
update {self.tblname} set first_name=\'测试查询test不阻塞\', last_name=\'测试%%不阻塞\' where id = 712;')
        self.log.info(result)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, result)
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, result)

        self.log.info('-------------------create table no relevance--------------------------------')
        result = self.primary_sh.execut_db_sql(
            f'DROP TABLE IF EXISTS {self.tblname_no_rel};CREATE TABLE {self.tblname_no_rel}(id INT, first_name text, last_name text);')
        self.log.info(result)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, result)
        self.log.info('-------------------insert data--------------------------------')
        result = self.primary_sh.execut_db_sql(f"INSERT INTO {self.tblname_no_rel} SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,8000000) AS id) AS x;\
update {self.tblname} set first_name='test 测试查询不阻塞', last_name='测试%%不阻塞' where id = 712;")
        self.log.info(result)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, result)
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, result)

        self.log.info(f'-----------------create index on {self.tblname}-----------------------------')
        sql = f"create index concurrently {self.idxname} on {self.tblname}  USING gin(to_tsvector('english', first_name));"
        create_index_thread = ComThread(self.primary_sh.execut_db_sql, args=(sql, ''))
        create_index_thread.setDaemon(True)
        create_index_thread.start()

        self.log.info(f'----------------- create index on {self.tblname_no_rel}-----------------------------')
        result = self.primary_sh.execut_db_sql(
            f"create index concurrently {self.idxname_no_rel} on {self.tblname_no_rel} USING gin(to_tsvector('english', first_name));")
        self.log.info(result)
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS, result)

        self.log.info('-----------------check create index result-----------------------------')
        create_index_thread.join(10 * 60)
        create_idx_result = create_index_thread.get_result()
        self.log.info(create_idx_result)
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS, create_idx_result)

        self.log.info(f'-----------------show {self.idxname}----------------------------')
        result = self.primary_sh.execut_db_sql(
            f"SET ENABLE_SEQSCAN=off;explain SELECT * FROM {self.idxname} where to_tsvector('english',first_name)@@ to_tsquery('english', 'test');")
        self.log.info(result)
        self.assertIn(self.idxname, result)

        self.log.info(f'-----------------select {self.idxname_no_rel}-----------------------------')
        result = self.primary_sh.execut_db_sql(
            f"SET ENABLE_SEQSCAN=off;explain SELECT * FROM {self.tblname_no_rel} where to_tsvector('english',first_name)@@ to_tsquery('english', 'test');")
        self.log.info(result)
        self.assertIn(self.idxname_no_rel, result)

    def tearDown(self):
        self.log.info('----------------this is tearDown------------------------------------')
        self.log.info('----------------drop table------------------------------------')
        result = self.primary_sh.execut_db_sql(f'drop table if exists {self.tblname};')
        self.log.info(result)
        result = self.primary_sh.execut_db_sql(f'drop table if exists {self.tblname_no_rel};')
        self.log.info(result)
