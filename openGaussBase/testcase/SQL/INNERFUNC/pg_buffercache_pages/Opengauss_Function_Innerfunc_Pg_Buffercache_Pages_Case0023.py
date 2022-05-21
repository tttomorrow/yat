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
Case Type   : pg_buffercache_pages函数功能
Case Name   : pg_buffercache_pages函数，索引对象pinning_backends字段验证
Description :
    1.gsql连接数据库，创建表及索引
    2.初始查询表的缓存信息
    3.表中插入一定量数据（5个会话同时执行）
    4.步骤3过程中循环查询表的缓存信息
    5.清理环境
Expect      :
    1、gsql连接数据库，创建表及索引成功
    2、初始查询表的索引缓存信息，为空（查询出的缓存记录为0行）;
    3、表中插入一定量数据成功
    4、再次查询表的索引缓存信息，pinning_backends字段存在大于0的场景
    5、清理环境成功
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class PgBuffercachePagesCase0023(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0023:初始化')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_sh2 = CommonSH('PrimaryDbUser')
        self.pri_sh3 = CommonSH('PrimaryDbUser')
        self.pri_sh4 = CommonSH('PrimaryDbUser')
        self.pri_sh5 = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.t_name1 = 't_pg_buffercache_pages_case0023'
        self.i_name1 = 'i_pg_buffercache_pages_case0023'

    def test_main(self):
        step_txt = '----step1: 创建表和索引，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.t_name1};' \
            f'create table {self.t_name1}(id int,content text);' \
            f'create index {self.i_name1} on {self.t_name1}(id);'
        self.log.info(create_sql)
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_result,
                      '执行失败：' + step_txt)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS, create_result,
                      '执行失败:' + step_txt)

        step2_txt = '----step2:初始查询表的缓存信息 expect: 为空---'
        self.log.info(step2_txt)
        select_sql = f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select relfilenode from pg_class " \
            f"where relname='{self.i_name1}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_count1 = int(select_result.strip().splitlines()[-2])
        self.assertEqual(tmp_count1, 0, '执行失败：' + step_txt)

        step3_txt = '----step3:表中插入一定量数据（5个会话同时执行） expect: 操作成功---'
        self.log.info(step3_txt)
        insert_sql = f"select now();" \
            f"insert into {self.t_name1} values(generate_series(1,1000000), " \
            f"'testtext');" \
            f"select now();"
        self.log.info(insert_sql)
        session1 = ComThread(self.pri_sh.execut_db_sql, args=(insert_sql,))
        session1.setDaemon(True)
        session1.start()

        session2 = ComThread(self.pri_sh2.execut_db_sql, args=(insert_sql,))
        session2.setDaemon(True)
        session2.start()

        session3 = ComThread(self.pri_sh3.execut_db_sql, args=(insert_sql,))
        session3.setDaemon(True)
        session3.start()

        session4 = ComThread(self.pri_sh4.execut_db_sql, args=(insert_sql,))
        session4.setDaemon(True)
        session4.start()

        session5 = ComThread(self.pri_sh5.execut_db_sql, args=(insert_sql,))
        session5.setDaemon(True)
        session5.start()

        step4_txt = '----step4: 步骤3过程中循环查询表的缓存信息' \
                    'expect:pinning_backends字段存在大于0的场景---'
        self.log.info(step4_txt)
        cnt = 0
        for i in range(30):
            select_sql = f"select count(*) from pg_buffercache_pages() " \
                f"where relfilenode in (select relfilenode from pg_class " \
                f"where relname='{self.i_name1}')  and pinning_backends >0;"
            self.log.info(select_sql)
            select_result1 = self.pri_sh.execut_db_sql(select_sql)
            self.log.info(select_result1)
            num = int(select_result1.strip().splitlines()[-2].strip())
            self.log.info(num)
            time.sleep(1)
            if num > 0:
                cnt += 1
                self.log.info("pinning_backends大于0的计数情况: " + str(cnt))

        self.assertGreater(cnt, 0, '执行失败:' + step4_txt)

        self.log.info('step 3 断言信息')
        session1.join(10 * 60)
        result1 = session1.get_result()
        self.log.info(result1)
        session2.join(10 * 60)
        result2 = session2.get_result()
        self.log.info(result2)
        session3.join(10 * 60)
        result3 = session3.get_result()
        self.log.info(result3)
        session4.join(10 * 60)
        result4 = session4.get_result()
        self.log.info(result4)
        session5.join(10 * 60)
        result5 = session5.get_result()
        self.log.info(result5)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result1,
                      '执行失败：' + step_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result2,
                      '执行失败：' + step_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result3,
                      '执行失败：' + step_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result4,
                      '执行失败：' + step_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result5,
                      '执行失败：' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step5: 清理环境,expect:环境清理成功----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t_name1};'
        self.log.info(drop_sql)
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_result,
                      '执行失败:' + step_txt)
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0023:执行完毕')
