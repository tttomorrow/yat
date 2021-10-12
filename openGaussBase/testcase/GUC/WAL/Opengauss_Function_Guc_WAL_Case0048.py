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
Case Name   : 修改checkpoint_warning为6min，观察预期结果；
Description :
    1、查询checkpoint_warning默认值；
    show checkpoint_warning;
    2、修改checkpoint_warning为6min，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "checkpoint_warning=6min"
    gs_om -t stop && gs_om -t start
    show checkpoint_warning;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为6min；
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
        logger.info("==Opengauss_Function_Guc_WAL_Case0048开始执行==")
        self.constant = Constant()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc_wal(self):
        logger.info("查询checkpoint_warning 期望：默认值5min")
        sql_cmd = COMMONSH.execut_db_sql("show checkpoint_warning;")
        logger.info(sql_cmd)
        self.assertIn("5min", sql_cmd)

        logger.info("方式一修改checkpoint_warning为6min，"
                    "重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'checkpoint_warning=6min')
        self.assertTrue(result)

        logger.info("期望：重启后查询结果为6min")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql("show checkpoint_warning;")
        logger.info(sql_cmd)
        self.assertIn("6min", sql_cmd)

        logger.info("创建表，期望：创建成功")
        sql_cmd = COMMONSH.execut_db_sql(f"drop table if exists test "
                                       f"cascade;"
                                       f"create table test(x int);")
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
                                       'checkpoint_warning=5min')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        logger.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show checkpoint_warning;")
        if "5min" not in sql_cmd:
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  'checkpoint_warning=5min')
            COMMONSH.restart_db_cluster()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("==Opengauss_Function_Guc_WAL_Case0048执行结束==")
