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
Case Name   : 修改autovacuum_vacuum_cost_delay，观察其预期结果
Description :
            1、查询autovacuum_vacuum_cost_delay默认值；
            show autovacuum_vacuum_cost_delay；
            2、修改autovacuum_vacuum_cost_delay为0，
            重启使其生效，观察预期结果；
            gs_guc set -D {cluster/dn1}
            -c "autovacuum_vacuum_cost_delay=50ms"
            3、恢复默认值；
Expect      :
            1、显示默认值；
            2、修改成功并生效
            预期结果正常；
            3、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

LOGGER = Logger()
COMMONSH = CommonSH('PrimaryDbUser')


class GuctestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Guc_Autovacuum_Case0025开始执行==")
        self.constant = Constant()
        self.db_user_node = Node('PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("查询autovacuum_vacuum_cost_delay "
                    "期望：默认值20ms")
        sql_cmd = COMMONSH.execut_db_sql(
            '''show autovacuum_vacuum_cost_delay;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("20ms", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("修改autovacuum_vacuum_cost_delay为50ms"
                    "重启生效，期望设置成功")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'autovacuum_vacuum_cost_delay=50ms')
        self.assertTrue(result)

        LOGGER.info("期望：重启后查询结果为50ms")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql(
            '''show autovacuum_vacuum_cost_delay;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("50ms", sql_cmd.split("\n")[-2].strip())

        LOGGER.info('做DML')
        sql_cmd = COMMONSH.execut_db_sql('''
                drop table if exists test cascade;
                create table test(c_int int);
                begin
                    for i in 0..100 loop
                        insert into test values(i);
                        update test set c_int = 66 where c_int = i;
                    end loop;
                end;
                select count(*) from test;
                ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        LOGGER.info("恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql(
            '''drop table if exists test cascade;''')
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'autovacuum_vacuum_cost_delay=20ms')
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
        sql_cmd = COMMONSH.execut_db_sql(
            '''show autovacuum_vacuum_cost_delay;''')
        if "20ms" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                  'autovacuum_vacuum_cost_delay=20ms')
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        result1 = COMMONSH.execute_gsguc('check', '20ms',
                                        'autovacuum_vacuum_cost_delay')
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.assertTrue(result1)
        LOGGER.info("==Guc_Autovacuum_Case0025执行结束==")
