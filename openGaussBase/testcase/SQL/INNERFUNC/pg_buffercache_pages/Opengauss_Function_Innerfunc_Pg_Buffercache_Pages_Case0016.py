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
Case Name   : pg_buffercache_pages函数，索引对象reltablespace字段验证
Description :
    1、gsql连接数据库，创建表及索引，一个默认表空间，一个指定表空间
    2、初始查询两张表索引的缓存信息
    3、两张表中插入不同量数据
    4、再次查询两张表索引的缓存信息，同时查询reltablespace信息
    5、查询两张表索引的表空间oid
    6、环境清理
Expect      :
    1、gsql连接数据库，创建表及索引,一个默认表空间，一个指定表空间，创建成功
    2、初始查询两张表索引的缓存信息，为空（查询出的缓存记录为0行）
    3、两张表索引中插入不同量数据，插入成功
    4、再次查询两张表索引的缓存信息，同时查询reltablespace信息，根据表的oid查询结果不为空，
       且数据量较大的表索引缓存数量大，两张表的reltablespace值不相同
    5、验证两张表索引表空间oid，与步骤4查询结果reltablespace字段一致
    6、环境清理成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class PgBuffercachePagesCase0016(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0016:初始化')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.ts_name1 = 'pg_default'
        self.ts_name2 = 'ts_pg_buffercache_pages_case0016'
        self.t_name1 = 't_pg_buffercache_pages_case0016_1'
        self.t_name2 = 't_pg_buffercache_pages_case0016_2'
        self.i_name1 = 'i_pg_buffercache_pages_case0016_1'
        self.i_name2 = 'i_pg_buffercache_pages_case0016_2'

    def test_main(self):
        step_txt = '----step1: 创建两张表及索引,一个默认表空间，一个指定表空间，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.t_name1}, {self.t_name2};' \
            f'create table {self.t_name1}(id int,content text);' \
            f'create index {self.i_name1} on {self.t_name1}(id);' \
            f"drop tablespace if exists {self.ts_name2};" \
            f"create tablespace {self.ts_name2} " \
            f"relative location '{self.ts_name2}'; " \
            f"create table {self.t_name2}(id int,content text)" \
            f" tablespace {self.ts_name2} ;" \
            f"create index {self.i_name2} on {self.t_name2}(id) " \
            f"tablespace {self.ts_name2} ;"
        self.log.info(create_sql)
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)

        tmp1 = create_result.strip().splitlines()[3].strip()
        tmp2 = create_result.strip().splitlines()[8].strip()
        self.assertEqual(tmp1, 'CREATE TABLE', '执行失败:' + step_txt)
        self.assertEqual(tmp2, 'CREATE TABLE', '执行失败:' + step_txt)
        self.assertTrue(create_result.count(self.constant.CREATE_INDEX_SUCCESS)
                        == 2, '执行失败:' + step_txt)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      '执行失败:' + step_txt)

        step_txt = '----step2: 初始查询两张表索引的缓存信息，expect: 均为0行----'
        self.log.info(step_txt)
        select_sql = f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select relfilenode from pg_class " \
            f"where relname in('{self.t_name1}','{self.t_name2}'));"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_count = int(select_result.strip().splitlines()[-2])
        self.assertEqual(tmp_count, 0, '执行失败：' + step_txt)

        step_txt = '----step3:两张表索引中插入不同量数据，expect: 插入成功----'
        self.log.info(step_txt)
        insert_sql = f"insert into {self.t_name1} " \
            f"values(generate_series(1, 1000), 'testtext');" \
            f"insert into {self.t_name2} " \
            f"values(generate_series(1, 10000), 'testtext');"
        self.log.info(insert_sql)
        insert_result = self.pri_sh.execut_db_sql(insert_sql)
        self.log.info(insert_result)
        self.assertTrue(insert_result.count(self.constant.INSERT_SUCCESS_MSG)
                        == 2, '执行失败:' + step_txt)

        step_txt = '----step4: 再次查询两张表索引的缓存信息，同时查询reltablespace字段' \
                   '，expect: 根据表的oid查询结果不为空，且数据量较大的表索引缓存数量大' \
                   '，且两张表的reltablespace不同----'
        self.log.info(step_txt)
        select_sql = f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.i_name1}') ;" \
            f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.i_name2}') ;"
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        t1_count = select_result.strip().splitlines()[2].strip()
        t2_count = select_result.strip().splitlines()[7].strip()
        self.assertNotEqual(t1_count, '', '执行失败，结果为空' + step_txt)
        self.assertNotEqual(t2_count, '', '执行失败，结果为空' + step_txt)
        self.assertGreater(int(t2_count), int(t1_count), '执行失败：' + step_txt)
        select_sql = f"select distinct reltablespace " \
            f"from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.i_name1}');" \
            f"select distinct reltablespace " \
            f"from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.i_name2}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_ts_oid1 = select_result.strip().splitlines()[2].strip()
        tmp_ts_oid2 = select_result.strip().splitlines()[7].strip()
        self.assertNotEqual(tmp_ts_oid1, tmp_ts_oid2, '执行失败：' + step_txt)

        step_txt = '--step5:验证两张表索引表空间oid ，expect: 与步骤4查询结果reltablespace字段一致--'
        self.log.info(step_txt)
        select_sql = f"select oid from pg_tablespace " \
            f"where spcname = '{self.ts_name1}';" \
            f"select oid from pg_tablespace " \
            f"where spcname = '{self.ts_name2}';"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        ts_oid1 = select_result.strip().splitlines()[2].strip()
        ts_oid2 = select_result.strip().splitlines()[7].strip()
        self.assertEqual(ts_oid1, tmp_ts_oid1, '执行失败：' + step_txt)
        self.assertEqual(ts_oid2, tmp_ts_oid2, '执行失败：' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step6: 清理环境，expect: 环境清理成功----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t_name1},{self.t_name2};' \
            f'drop tablespace if exists {self.ts_name2}; '
        self.log.info(drop_sql)
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_result,
                      '执行失败：' + step_txt)
        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS, drop_result,
                      '执行失败:' + step_txt)
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0016:执行完毕')
