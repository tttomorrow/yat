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
Case Name   : 修改recovery_parse_workers为2，观察预期结果；
Description :
    1、查询recovery_parse_workers、replication_type、hot_standby默认值；
    show recovery_parse_workers;1
    show hot_standby;on
    show replication_type;1
    2、hot_standby设置成off，replication_type设置成1重启生效后，
    recovery_parse_workers为2，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "hot_standby=off"
    gs_om -t stop && gs_om -t start
    gs_guc set -D {cluster/dn1} -c "recovery_parse_workers=2"
    gs_om -t stop && gs_om -t start
    show recovery_parse_workers;
    3、重启后执行简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为2；
    3、DML无报错
    4、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
COMMONSH = CommonSH('PrimaryDbUser')


class Guctestcase(unittest.TestCase):
    def setUp(self):
        logger.info("==Opengauss_Function_Guc_WAL_Case0064开始执行==")
        self.constant = Constant()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc_wal(self):
        logger.info("查询recovery_parse_workers 期望：默认值1")
        sql_cmd = COMMONSH.execut_db_sql("show recovery_parse_workers;")
        logger.info(sql_cmd)
        self.assertIn("1", sql_cmd)
        sql_cmd = COMMONSH.execut_db_sql("show hot_standby;")
        logger.info(sql_cmd)
        self.assertIn(self.constant.OPEN_STATUS_MSG[0], sql_cmd)
        sql_cmd = COMMONSH.execut_db_sql("show replication_type;")
        logger.info(sql_cmd)
        self.assertIn("1", sql_cmd)

        logger.info("方式一修改recovery_parse_workers为2，"
                    "重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'hot_standby=off')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("期望：重启后设置2 查询结果为2")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'recovery_parse_workers=2')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql("show recovery_parse_workers;")
        logger.info(sql_cmd)
        self.assertIn("2", sql_cmd)

        logger.info("创建表，期望：创建成功")
        sql_cmd = COMMONSH.execut_db_sql("drop table if exists test ;"
                                       "create table test(x int);")
        logger.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd)

        logger.info("恢复默认值")
        logger.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql("drop table test cascade;")
        logger.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'recovery_parse_workers=1')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'hot_standby=on')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        logger.info("恢复默认值")
        sql_cmd1 = COMMONSH.execut_db_sql("show recovery_parse_workers;")
        sql_cmd2 = COMMONSH.execut_db_sql("show hot_standby;")
        if ("1" not in sql_cmd1) or ("on" not in sql_cmd2):
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  'recovery_parse_workers=1')
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  'hot_standby=on')
            COMMONSH.restart_db_cluster()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("==Opengauss_Function_Guc_WAL_Case0064执行结束==")
