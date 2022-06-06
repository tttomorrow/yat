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
Case Type   : GUC
Case Name   : 修改autovacuum，观察其预期结果
Description :
            1、查询autovacuum默认值；
            show autovacuum；
            2、修改autovacuum为off，重启使其生效，观察预期结果；
            gs_guc set -D {cluster/dn1} -c "autovacuum=off"
            3、恢复默认值；
Expect      :
            1、显示默认值；
            2、修改参数后，系统不自动清理，当修改autovacuum为on后，
            autovacuum_max_workers大于0时，系统不仅在故障恢复后，
            自动清理两阶段事务，并且还可以自动清理进程。预期结果正常；
            3、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH('PrimaryDbUser')


class GuctestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Guc_Autovacuum_Case0001开始执行==")
        self.constant = Constant()
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_guc(self):
        LOGGER.info("查询autovacuum 期望：默认值on")
        sql_cmd = COMMONSH.execut_db_sql('''show autovacuum;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("修改autovacuum为off，重启生效，期望：设置成功")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       'autovacuum=off')
        self.assertTrue(result)

        LOGGER.info("期望：重启后查询结果为off")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql('''show autovacuum;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.split("\n")[-2].strip())

        LOGGER.info('做DML')
        sql_cmd = COMMONSH.execut_db_sql('''
                drop table if exists test cascade;
                create table test(c_int int);
                begin
                    for i in 0..10000 loop
                        insert into test values(i);
                    end loop;
                end;
                select count(*) from test;
                ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        LOGGER.info("修改autovacuum_naptime为60，期望：设置成功")
        result = COMMONSH.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'autovacuum_naptime=60')
        self.assertTrue(result)

        LOGGER.info("删除表后等待1min查看不执行自动清理")
        result = COMMONSH.execut_db_sql('''delete from test;
        select pg_sleep(60);select pg_stat_get_vacuum_count(a.oid)  \
        from pg_class  a where a.relname = 'test';''')
        LOGGER.info(result)
        self.assertEqual(int(result.split("\n")[-2].strip()), 0)

        LOGGER.info("恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql(
            '''drop table if exists test cascade;''')
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       'autovacuum=on')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       'autovacuum_naptime=10min')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql(
            '''drop table if exists test cascade;''')
        LOGGER.info(sql_cmd)
        sql_cmd = COMMONSH.execut_db_sql('''show autovacuum;''')
        if "on" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                  'autovacuum=on')
            COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                  'autovacuum_naptime=10min')
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        result1 = COMMONSH.execute_gsguc('check', 'on', 'autovacuum')
        result2 = COMMONSH.execute_gsguc('check', '10min',
                                        'autovacuum_naptime')
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.assertTrue(result1)
        self.assertTrue(result2)
        LOGGER.info("==Guc_Autovacuum_Case0001执行结束==")
