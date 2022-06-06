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
Case Type   : pg_buffercache_pages验证
Case Name   : pg_buffercache_pages函数，表对象reldatabase字段验证
Description :
    1、gsql连接数据库，创建表及索引，两张表不同库
    2、初始查询两张表索引的缓存信息
    3、两张表中插入不同量数据
    4、再次查询两张表索引的缓存信息
    5、查询两张表的数据库oid
    6、清理环境
Expect      :
    1、gsql连接数据库，创建表，两张表不同库，创建成功
    2、初始查询两张表的缓存信息，为空（查询出的缓存记录为0行）
    3、两张表中插入不同量数据，插入成功
    4、再次查询两张表的缓存信息，根据表的oid查询结果不为空，且数据量较大的表缓存数量大
    5、查询两张表的数据库oid，与步骤4查询结果reldatabase字段一致
    6、清理环境成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class PgBuffercachePagesCase0017(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0017:初始化')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.db_name2 = 'db_pg_buffercache_pages_case0017'
        self.t_name1 = 't_pg_buffercache_pages_case0017_1'
        self.t_name2 = 't_pg_buffercache_pages_case0017_2'
        self.i_name1 = 'i_pg_buffercache_pages_case0017_1'
        self.i_name2 = 'i_pg_buffercache_pages_case0017_2'

    def test_main(self):
        step_txt = '----step1:创建表及索引，两张表不同库，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.t_name1};' \
            f'create table {self.t_name1}(id int,content text);' \
            f'create index {self.i_name1} on {self.t_name1}(id);' \
            f'drop database if exists {self.db_name2};' \
            f'create database {self.db_name2};'
        self.log.info(create_sql)
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_result,
                      '执行失败:' + step_txt)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS, create_result,
                      '执行失败:' + step_txt)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, create_result,
                      '执行失败:' + step_txt)

        create_sql = f'create table {self.t_name2}(id int,content text);' \
            f'create index {self.i_name2} on {self.t_name2}(id);'
        self.log.info(create_sql)
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  dbname=f'{self.db_name2}')
        self.log.info(create_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_result,
                      '执行失败:' + step_txt)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS, create_result,
                      '执行失败:' + step_txt)

        step_txt = '----step2: 初始查询两张表的缓存信息，expect: 均为0行----'
        self.log.info(step_txt)
        select_sql = f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.i_name1}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_count1 = int(select_result.strip().splitlines()[-2])
        self.assertEqual(tmp_count1, 0, '执行失败：' + step_txt)
        select_sql = f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.i_name2}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql,
                                                  dbname=f'{self.db_name2}')
        self.log.info(select_result)
        tmp_count2 = int(select_result.strip().splitlines()[-2])
        self.assertEqual(tmp_count2, 0, '执行失败：' + step_txt)

        step_txt = '----step3:两张表中插入不同量数据，expect: 插入成功----'
        self.log.info(step_txt)
        insert_sql = f"insert into {self.t_name1} " \
            f"values(generate_series(1, 1000), 'testtext');"
        self.log.info(insert_sql)
        insert_result = self.pri_sh.execut_db_sql(insert_sql)
        self.log.info(insert_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_result,
                      '执行失败:' + step_txt)

        insert_sql = f"insert into {self.t_name2} " \
            f"values(generate_series(1, 10000), 'testtext');"
        self.log.info(insert_sql)
        insert_result = self.pri_sh.execut_db_sql(insert_sql,
                                                  dbname=f'{self.db_name2}')
        self.log.info(insert_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_result,
                      '执行失败:' + step_txt)

        step_txt = '----step4: 再次查询两张表的缓存信息，expect: ' \
                   '根据表的oid查询结果不为空，且数据量较大的表缓存数量大----'
        self.log.info(step_txt)
        select_sql = f"select count(*) " \
            f"from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.i_name1}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        null_flag1 = select_result.strip().splitlines()[-2].strip()
        self.assertNotEqual(null_flag1, '0', '执行失败，结果为空' + step_txt)

        select_sql = f"select count(*) " \
            f"from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.i_name2}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql,
                                                  dbname=f'{self.db_name2}')
        self.log.info(select_result)
        null_flag2 = select_result.strip().splitlines()[-2].strip()
        self.assertNotEqual(null_flag2, '0', '执行失败，结果为空' + step_txt)

        self.assertGreater(int(null_flag2), int(null_flag1), '执行失败' + step_txt)

        select_sql = f"select distinct reldatabase " \
            f"from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.i_name1}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_db_oid1 = select_result.strip().splitlines()[-2].strip()

        select_sql = f"select distinct reldatabase " \
            f"from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.i_name2}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql,
                                                  dbname=f'{self.db_name2}')
        self.log.info(select_result)
        tmp_db_oid2 = select_result.strip().splitlines()[-2].strip()
        self.assertNotEqual(tmp_db_oid1, tmp_db_oid2, '执行失败：' + step_txt)

        step_txt = '--step5:查询两张表的数据库oid,expect: 与步骤4查询结果reldatabase字段一致--'
        self.log.info(step_txt)
        select_sql = f"select oid from pg_database  " \
            f"where datname  = '{self.pri_dbuser.db_name}';" \
            f"select oid from pg_database " \
            f"where datname = '{self.db_name2}';"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        db_oid1 = select_result.strip().splitlines()[2].strip()
        db_oid2 = select_result.strip().splitlines()[7].strip()
        self.assertEqual(db_oid1, tmp_db_oid1, '执行失败：' + step_txt)
        self.assertEqual(db_oid2, tmp_db_oid2, '执行失败：' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step6: 清理环境,expect:----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t_name1};' \
            f'drop database if exists {self.db_name2}; '
        self.log.info(drop_sql)
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_result,
                      '执行失败：' + step_txt)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, drop_result,
                      '执行失败：' + step_txt)
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0017:执行完毕')
