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
"""
Case Type   : 功能
Case Name   : 创建索引过程中在事务外对相关表进行select操作
Description :
    1.创建表，并插入大数据
    2.使用concurrently创建索引
    3.在创建索引的同时对表进行 select操作
    4.使用explain检查索引可否正常使用
    5、清理环境 删除表
Expect      :
    1、创建表插入数据成功
    2、concurrently创建索引成功
    3、select操作成功 select操作耗时小于创建索引耗时
    4、索引正常使用
    5、清理环境
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
        self.tblname = 'ddl_index_case0209'
        self.idxname = 'ddl_index_case0209_idx'
        self.log.info(
            '------------------------------------Opengauss_Function_ddl_index_case0209.py start------------------------------------')

    def test_in_select(self):
        self.log.info('-------------------create table--------------------------------')
        result = self.primary_sh.execut_db_sql(
            f'DROP TABLE IF EXISTS {self.tblname};CREATE TABLE {self.tblname}(id INT, first_name text, last_name text);')
        self.log.info(result)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, result)
        self.log.info('-------------------insert data--------------------------------')
        result = self.primary_sh.execut_db_sql(f'INSERT INTO {self.tblname} SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,8000000) AS id) AS x;\
update {self.tblname} set first_name=\'test hung^%\', last_name=\'123 test num \\\' where id = 712;')
        self.log.info(result)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, result)
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, result)

        self.log.info('-----------------create index-----------------------------')
        sql = f'select current_time;' \
              f'create index concurrently {self.idxname} on {self.tblname} ' \
              f'USING btree(id);select current_time;'
        create_index_thread = ComThread(self.primary_sh.execut_db_sql, args=(sql, ''))
        create_index_thread.setDaemon(True)
        create_index_thread.start()

        self.log.info('-----------------select table-----------------------------')
        result = self.primary_sh.execut_db_sql(f'SELECT * FROM '
            f'{self.tblname} where id = 712;'
            f'explain performance '
            f'SELECT * FROM {self.tblname} '
            f'where id = 712;')
        self.log.info(result)
        self.assertNotIn('ERROR', result)
        self.assertIn('test hung^%', result)
        self.assertIn('123 test num \\', result)
        self.assertIn('712', result)

        self.log.info("select耗时")
        select_time = float(result.splitlines()[-2].split()[2])
        self.log.info(select_time)
        self.log.info("select耗时小于10000ms")
        self.assertLess(select_time, 100000)

        self.log.info('---------check create index result---------')
        create_index_thread.join(10 * 60)
        create_idx_result = create_index_thread.get_result()
        self.log.info(create_idx_result)

        before_create_time = create_idx_result.splitlines()[2].strip()
        after_create_time = create_idx_result.splitlines()[-2].strip()
        self.log.info(f'before_create_time is {before_create_time}')
        self.log.info(f'after_create_time is {after_create_time}')
        create_time_H = before_create_time.split(':')[0]
        create_time_M = before_create_time.split(':')[1]
        create_time_S = before_create_time.split(':')[2].split('.')[0]
        create_time_H1 = after_create_time.split(':')[0]
        create_time_M1 = after_create_time.split(':')[1]
        create_time_S1 = after_create_time.split(':')[2].split('.')[0]
        create_index_time = int(create_time_H1) * 60 * 60 + int(create_time_M1) * 60 + int(create_time_S1) - int(
            create_time_H) * 60 * 60 - int(create_time_M) * 60 - int(create_time_S)
        self.log.info("创建索引耗时")
        self.log.info(f'create_index_time is {create_index_time}')
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS, create_idx_result)
        self.log.info("若阻塞查询时间必然比创建索引时间大，反之则不阻塞")
        self.assertTrue(create_index_time - select_time)

        self.log.info('-----------------explain select-----------------------------')
        result = self.primary_sh.execut_db_sql(
            f'SET ENABLE_SEQSCAN=off;explain SELECT * FROM {self.tblname} where  id = 712;;')
        self.log.info(result)
        self.assertIn(self.idxname, result)

    def tearDown(self):
        self.log.info('----------------this is tearDown------------------------------------')
        self.log.info('----------------drop table------------------------------------')
        result = self.primary_sh.execut_db_sql(f'RESET ENABLE_SEQSCAN;drop table if exists {self.tblname};')
        self.log.info(result)
