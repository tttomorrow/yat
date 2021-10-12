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
Case Name   : 修改instr_rt_percentile_interval为12345，观察预期结果；
Description :
    1、查询instr_rt_percentile_interval默认值；
    show instr_rt_percentile_interval;
    2、修改instr_rt_percentile_interval为12345，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "instr_rt_percentile_interval=12345"
    gs_om -t stop && gs_om -t start
    show instr_rt_percentile_interval;
    3、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改失败
    3、恢复默认值成功；
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
        logger.info("==Opengauss_Function_Guc_Query_Case0010开始执行==")
        self.constant = Constant()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc(self):
        logger.info("查询instr_rt_percentile_interval 期望：默认值on")
        sql_cmd = COMMONSH.execut_db_sql("show \
            instr_rt_percentile_interval;")
        logger.info(sql_cmd)
        self.assertIn("10", sql_cmd)

        logger.info("方式一修改instr_rt_percentile_interval为12345，"
                    "重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "instr_rt_percentile_interval=12345")
        self.assertFalse(result)

        logger.info("期望：重启后查询结果为1min")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql("show \
            instr_rt_percentile_interval;")
        logger.info(sql_cmd)
        self.assertIn("10s", sql_cmd)

    def tearDown(self):
        logger.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show \
                instr_rt_percentile_interval;")
        if "10s" not in sql_cmd:
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  "instr_rt_percentile_interval=10")
            COMMONSH.restart_db_cluster()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("==Opengauss_Function_Guc_Query_Case0010执行结束==")
