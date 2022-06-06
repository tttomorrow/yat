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
Case Name   : pg_buffercache_pages函数，表对象relforknumber字段验证
Description :
    1、gsql连接数据库，创建表
    2、初始查询表的缓存信息
    3、表中插入不同量数据
    4、再次查询表的缓存信息
    5、清理环境
Expect      :
    1、gsql连接数据库，创建表成功
    2、初始查询表的缓存信息，为空;
    3、表中插入不同量数据成功
    4、再次查询表的缓存信息，数据量较大的表查询结果relforknumber查询结果存在0，1，数据量较小表查询结果为0
    5、环境清理成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class PgBuffercachePagesCase0008(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0008:初始化')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.t_name1 = 't_pg_buffercache_pages_case0008_1'
        self.t_name2 = 't_pg_buffercache_pages_case0008_2'

    def test_main(self):
        step_txt = '----step1:连接数据库，创建表，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.t_name1},{self.t_name2};' \
            f'create table {self.t_name1}(id int,content text);' \
            f'create table {self.t_name2}(id int,content text);'
        self.log.info(create_sql)
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertTrue(create_result.count(self.constant.TABLE_CREATE_SUCCESS)
                        == 2, '执行失败:' + step_txt)

        step_txt = '----step2: 初始查询两张表的缓存信息，expect: 均为0行----'
        self.log.info(step_txt)
        select_sql = f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select relfilenode from pg_class " \
            f"where relname in('{self.t_name1}','{self.t_name2}'));"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_count = int(select_result.strip().splitlines()[-2])
        self.assertEqual(tmp_count, 0, '执行失败：' + step_txt)

        step_txt = '----step3:两张表中插入不同量数据，expect: 插入成功----'
        self.log.info(step_txt)
        insert_sql = f"insert into {self.t_name1} " \
            f"values(generate_series(1, 1000), 'testtext');" \
            f"insert into {self.t_name2} " \
            f"values(generate_series(1, 10), 'testtext');"
        self.log.info(insert_sql)
        insert_result = self.pri_sh.execut_db_sql(insert_sql)
        self.log.info(insert_result)
        self.assertTrue(insert_result.count(self.constant.INSERT_SUCCESS_MSG)
                        == 2, '执行失败:' + step_txt)

        step_txt = f'----step4: 再次查询两张表的缓存信息，expect: ' \
            f'数据量较大的表查询结果relforknumber查询结果存在0，1，' \
            f'数据量较小表查询结果为0----'
        self.log.info(step_txt)
        select_sql = f"select distinct relforknumber from " \
            f"pg_buffercache_pages() where relfilenode in (select " \
            f"relfilenode from pg_class " \
            f"where relname='{self.t_name1}') order by 1;" \
            f"select distinct relforknumber from pg_buffercache_pages() " \
            f"where relfilenode in (select relfilenode from pg_class " \
            f"where relname='{self.t_name2}') order by 1;"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        t1_count1 = select_result.strip().splitlines()[2].strip()
        t1_count2 = select_result.strip().splitlines()[3].strip()
        t2_count = select_result.strip().splitlines()[-2].strip()
        self.assertEqual(t1_count1, '0', '执行失败：' + step_txt)
        self.assertEqual(t1_count2, '1', '执行失败：' + step_txt)
        self.assertEqual(t2_count, '0', '执行失败：' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step5: 环境清理，expect:清理成功----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t_name1};' \
            f'drop table if exists {self.t_name2}; '
        self.log.info(drop_sql)
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        self.assertTrue(drop_result.count(self.constant.TABLE_DROP_SUCCESS)
                        == 2, '执行失败:' + step_txt)
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0008:执行完毕')
