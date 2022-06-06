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
Case Name   : pg_buffercache_pages函数，索引对象relfilenode字段验证
Description :
    1、gsql连接数据库，创建表及索引
    2、初始查询两张表索引的缓存信息
    3、两张表中插入不同量数据
    4、再次查询两张表索引的缓存信息
    5、清理环境
Expect      :
    1、gsql连接数据库，创建表及索引，创建成功
    2、初始查询两张表索引的缓存信息，为空（查询出的缓存记录为0行）
    3、两张表中插入不同量数据，插入成功
    4、再次查询两张表索引的缓存信息，根据索引的oid查询结果不为空，且数据量较大的表索引缓存数量大
    5、清理环境成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class PgBuffercachePagesCase0015(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0015:初始化')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.t_name1 = 't_pg_buffercache_pages_case0015_1'
        self.t_name2 = 't_pg_buffercache_pages_case0015_2'
        self.t_index1 = 'i_pg_buffercache_pages_case0015_1'
        self.t_index2 = 'i_pg_buffercache_pages_case0015_2'

    def test_main(self):
        step_txt = '----step1: 创建两张表和索引，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.t_name1},{self.t_name2};' \
            f'create table {self.t_name1}(id int,name text);' \
            f'create table {self.t_name2}(id int,name text);' \
            f'create index {self.t_index1} on {self.t_name1}(id);' \
            f'create index {self.t_index2} on {self.t_name2}(id);'
        self.log.info(create_sql)
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertTrue(create_result.count(self.constant.TABLE_CREATE_SUCCESS)
                        == 2, '执行失败:' + step_txt)
        self.assertTrue(create_result.count(self.constant.CREATE_INDEX_SUCCESS)
                        == 2, '执行失败:' + step_txt)

        step_txt = '----step2: 初始查询两张表索引的缓存信息，expect: 均为0行----'
        self.log.info(step_txt)
        select_sql = f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.t_index1}');" \
            f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.t_index2}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        i1_count = select_result.strip().splitlines()[2].strip()
        i2_count = select_result.strip().splitlines()[7].strip()
        self.assertEqual(i1_count, '0', '执行失败：' + step_txt)
        self.assertEqual(i2_count, '0', '执行失败：' + step_txt)

        step_txt = '----step3:两张表中插入不同量数据，expect: 插入成功----'
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

        step_txt = '----step4: 再次查询两张表的缓存信息，expect: ' \
                   '根据索引的oid查询结果不为空，且数据量较大的表索引缓存数量大----'
        self.log.info(step_txt)
        select_sql = f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.t_index1}');" \
            "select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select oid from pg_class " \
            f"where relname='{self.t_index2}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        t1_count = select_result.strip().splitlines()[2].strip()
        t2_count = select_result.strip().splitlines()[7].strip()
        self.assertNotEqual(t1_count, '', '执行失败，结果为空' + step_txt)
        self.assertNotEqual(t2_count, '', '执行失败，结果为空' + step_txt)
        self.assertGreater(int(t2_count), int(t1_count), '执行失败：' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step5: 清理环境，expect:清理环境成功----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t_name1};' \
            f'drop table if exists {self.t_name2};'
        self.log.info(drop_sql)
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        self.assertTrue(drop_result.count(self.constant.TABLE_DROP_SUCCESS)
                        == 2, '执行失败:' + step_txt)
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0015:执行完毕')
