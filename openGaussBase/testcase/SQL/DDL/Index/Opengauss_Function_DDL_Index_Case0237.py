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
Case Name   : 同一表上并行创建普通索引和concurrently索引
Description :
    1.创建表a，并插入数据
    2.并发创建concurrently索引
Expect      :
    1.创建表并插入数据成功
    2.创建索引失败，产生死锁（创建索引为5级锁）
History     :
"""

import unittest
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
        self.tblname = 'ddl_index_case0237'
        self.idxname = 'ddl_index_case0237_idx'
        self.idxname1 = 'ddl_index_case0237_idx1'
        self.log.info(
            '------------------------------------Opengauss_Function_DDL_Index_Case0237.py start------------------------------------')

    def test_in_select(self):
        self.log.info('-------------------create table--------------------------------')
        result = self.primary_sh.execut_db_sql(
            f'DROP TABLE IF EXISTS {self.tblname};CREATE TABLE {self.tblname}(id INT, first_name text, last_name text);')
        self.log.info(result)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, result)
        self.log.info('-------------------insert data--------------------------------')
        result = self.primary_sh.execut_db_sql(f'INSERT INTO {self.tblname} SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,8000000) AS id) AS x;\
update {self.tblname} set first_name=\'测试查询不阻塞\', last_name=\'测试%%不阻塞\' where id = 712;')
        self.log.info(result)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, result)
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, result)

        self.log.info('-----------------create index concurrently-----------------------------')
        sql = f'create index concurrently {self.idxname} on {self.tblname} using btree(id);'
        create_index_thread = ComThread(self.primary_sh.execut_db_sql, args=(sql, ''))
        create_index_thread.setDaemon(True)
        create_index_thread.start()

        self.log.info('-----------------create index-----------------------------')
        result = self.primary_sh.execut_db_sql(f'create index  {self.idxname1} on {self.tblname} using btree(id);')
        self.log.info(result)

        self.log.info('-----------------check create index result-----------------------------')
        create_index_thread.join(20 * 60)
        create_idx_result = create_index_thread.get_result()
        self.log.info(create_idx_result)
        self.assertTrue(
            (self.Constant.CREATE_INDEX_SUCCESS in result) or (self.Constant.CREATE_INDEX_SUCCESS in create_idx_result))

    def tearDown(self):
        self.log.info('----------------this is tearDown------------------------------------')
        self.log.info('----------------drop table------------------------------------')
        result = self.primary_sh.execut_db_sql(f'drop table if exists {self.tblname};')
        self.log.info(result)
