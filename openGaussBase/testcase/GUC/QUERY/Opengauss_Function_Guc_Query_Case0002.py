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
Case Name   : 修改instr_unique_sql_count为false 'test'，观察预期结果；
Description :
    1、查询instr_unique_sql_count默认值；
    show instr_unique_sql_count;
    2、修改instr_unique_sql_count为false 'test'，重启
    gs_guc set -D {cluster/dn1} -c "instr_unique_sql_count=false"
    gs_guc set -D {cluster/dn1} -c "instr_unique_sql_count='test'"
    gs_om -t stop && gs_om -t start
    show instr_unique_sql_count;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为false 'test'；
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
        logger.info("==Opengauss_Function_Guc_Query_Case0002开始执行==")
        self.constant = Constant()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc(self):
        logger.info("查询instr_unique_sql_count 期望：默认值100")
        sql_cmd = COMMONSH.execut_db_sql("show instr_unique_sql_count;")
        logger.info(sql_cmd)
        self.assertIn("100", sql_cmd)

        logger.info("方式一修改instr_unique_sql_count为'test'，"
                    "重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "instr_unique_sql_count='test'")
        self.assertFalse(result)

        logger.info("方式一修改instr_unique_sql_count为false"
                    "重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "instr_unique_sql_count=false")
        self.assertFalse(result)

    def tearDown(self):
        logger.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show instr_unique_sql_count;")
        if "100" not in sql_cmd:
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  "instr_unique_sql_count=100")
            COMMONSH.restart_db_cluster()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("==Opengauss_Function_Guc_Query_Case0002执行结束==")
