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
Case Type   : GUC
Case Name   : 修改defer_csn_cleanup_time，观察其预期结果
Description :
            1、查询defer_csn_cleanup_time默认值；
            show defer_csn_cleanup_time；
            2、修改defer_csn_cleanup_time为0，重启使其生效，观察预期结果；
            gs_guc set -D {cluster/dn1}  -c "defer_csn_cleanup_time=10000"
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
        LOGGER.info("==Guc_Autovacuum_Case0029开始执行==")
        self.constant = Constant()
        self.db_user_node = Node('PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("查询defer_csn_cleanup_time "
                    "期望：默认值5s")
        sql_cmd = COMMONSH.execut_db_sql(
            '''show defer_csn_cleanup_time;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("5s", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("修改defer_csn_cleanup_time为10000"
                    "重启生效，期望设置成功")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       'defer_csn_cleanup_time=10000')
        self.assertTrue(result)

        LOGGER.info("期望：重启后查询结果为10s")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql(
            '''show defer_csn_cleanup_time;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("10s", sql_cmd.split("\n")[-2].strip())

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
            'defer_csn_cleanup_time=5s')
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
            '''show defer_csn_cleanup_time;''')
        if "5s" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                  'defer_csn_cleanup_time=5s')
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        result1 = COMMONSH.execute_gsguc('check', '5s',
                                        'defer_csn_cleanup_time')
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.assertTrue(result1)
        LOGGER.info("==Guc_Autovacuum_Case0029执行结束==")
