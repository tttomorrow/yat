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
Case Name   : 修改instr_unique_sql_count为off，观察预期结果；
Description :
    1、查询instr_unique_sql_count默认值；
    show instr_unique_sql_count;
    2、修改instr_unique_sql_count为off，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "instr_unique_sql_count=off"
    gs_om -t stop && gs_om -t start
    show instr_unique_sql_count;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为off；
    3、DML无报错
    4、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class Guctestcase(unittest.TestCase):
    def setUp(self):
        logger.info("==Opengauss_Function_Guc_Query_Case0001开始执行==")
        self.constant = Constant()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc(self):
        logger.info("查询instr_unique_sql_count 期望：默认值100")
        sql_cmd = COMMONSH.execut_db_sql("show instr_unique_sql_count;")
        logger.info(sql_cmd)
        self.assertIn("100", sql_cmd)

        logger.info("方式一修改instr_unique_sql_count为1，"
                    "重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "instr_unique_sql_count=1")
        self.assertTrue(result)

        logger.info("期望：重启后查询结果为1")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql("show instr_unique_sql_count;")
        logger.info(sql_cmd)
        self.assertIn("1", sql_cmd)

        logger.info("创建表，期望：创建成功")
        sql_cmd = COMMONSH.execut_db_sql("drop table if exists test;\
            create table test(x int);")
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
                                       "instr_unique_sql_count=100")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        logger.info("恢复默认值")
        logger.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql("drop table if exists test;")
        logger.info(sql_cmd)
        sql_cmd = COMMONSH.execut_db_sql("show instr_unique_sql_count;")
        if "100" not in sql_cmd:
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  "instr_unique_sql_count=100")
            COMMONSH.restart_db_cluster()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("==Opengauss_Function_Guc_Query_Case0001执行结束==")
