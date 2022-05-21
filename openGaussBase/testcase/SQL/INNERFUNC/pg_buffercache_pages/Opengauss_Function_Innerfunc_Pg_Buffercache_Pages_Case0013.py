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
Case Name   : pg_buffercache_pages函数，表对象isvalid字段验证
Description :
    1、重启数据库后，gsql连接数据库，查询isvalid为f的的缓冲区
    2、gsql连接数据库，创建表
    3、初始查询表的缓存信息
    4、表中插入一定量数据
    5、再次查询表的缓存信息
    6、环境清理
Expect      :
    1、重启数据库后，gsql连接数据库，查询isvalid为f的的缓冲区，为未使用缓冲区，除了isvalid和bufferid字段外，其余为空
    2、gsql连接数据库，创建表成功
    3、初始查询表的缓存信息，为空（查询出的缓存记录为0行）;
    4、表中插入一定量数据成功
    5、再次查询表的缓存信息，isvalid字段均为t
    6、环境清理成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class PgBuffercachePagesCase0013(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0013:初始化')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.t_name1 = 't_pg_buffercache_pages_case0013_1'
        restart_flag1 = self.pri_sh.restart_db_cluster()
        self.assertTrue(restart_flag1, '重启数据库失败')

    def test_main(self):
        step_txt = f'----step1:重启数据库后，查询isvalid为f的的缓冲区，' \
            f'expect: 查询isvalid为f的的缓冲区，为未使用缓冲区，' \
            f'除了isvalid和bufferid字段外，其余为空----'
        self.log.info(step_txt)
        select_sql = f'select case when count(*)=0 then null end ' \
            f'from pg_buffercache_pages() where ' \
            f'isvalid=false and bufferid is null;' \
            f'select distinct concat(relfilenode,bucketid,' \
            f'storage_type,reltablespace,reldatabase,relforknumber,' \
            f'relblocknumber,isdirty,usage_count,pinning_backends) ' \
            f'null_value from pg_buffercache_pages() where isvalid=false;'
        self.log.info(select_sql)
        null_value = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(null_value)
        t1_result1 = null_value.strip().splitlines()[2].strip()
        t1_result2 = null_value.strip().splitlines()[7].strip()
        self.assertEqual(t1_result1, '', '执行失败:' + step_txt)
        self.assertEqual(t1_result2, '', '执行失败:' + step_txt)

        step_txt = '----step2:创建一张表，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.t_name1};' \
            f'create table {self.t_name1}(id int,content text);'
        self.log.info(create_sql)
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_result,
                      '执行失败:' + step_txt)

        step_txt = '----step3: 初始查询表的缓存信息，expect: 为0行----'
        self.log.info(step_txt)
        select_sql = f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select relfilenode from pg_class " \
            f"where relname='{self.t_name1}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_count1 = int(select_result.strip().splitlines()[-2])
        self.assertEqual(tmp_count1, 0, '执行失败：' + step_txt)

        step_txt = '----step4:表中插入一定量的数据，expect: 插入成功----'
        self.log.info(step_txt)
        insert_sql = f"insert into {self.t_name1} " \
            f"values(generate_series(1, 1000), 'testtext');"
        self.log.info(insert_sql)
        insert_result = self.pri_sh.execut_db_sql(insert_sql)
        self.log.info(insert_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_result,
                      '执行失败:' + step_txt)

        step_txt = f'----step5: 再次查询表的缓存信息，expect: isdirty字段为t'
        self.log.info(step_txt)
        select_sql = f"select distinct isvalid from pg_buffercache_pages() " \
            f"where relfilenode in (select relfilenode from pg_class " \
            f"where relname='{self.t_name1}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        isdirty_flag = select_result.strip().splitlines()[-2].strip()
        self.assertEqual(isdirty_flag, 't', '执行失败：' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step6: 环境清理，expect:清理成功----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t_name1};'
        self.log.info(drop_sql)
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_result,
                      '执行失败：' + step_txt)
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0013:执行完毕')
