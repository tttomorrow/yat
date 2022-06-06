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
Case Name   : 方式二修改track_sql_count为0/false/no，观察预期结果；
Description :
    1、查询track_sql_count默认值；
    show track_sql_count;
    2、修改track_sql_count为on，重启使其生效，并校验其预期结果；
    gs_guc reload -D {cluster/dn1} -c "track_sql_count=0"
    gs_guc reload -D {cluster/dn1} -c "track_sql_count=false"
    gs_guc reload -D {cluster/dn1} -c "track_sql_count=no"
    gs_om -t stop && gs_om -t start
    show track_sql_count;
    3、恢复默认值；
Expect      :
    1、显示默认值 查询gs_sql_count视图不为空
    2、参数修改成功，校验修改后系统参数值为off
    3、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GucTestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0077开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("步骤1: 查询track_sql_count 期望：默认值on")
        sql_cmd = COMMONSH.execut_db_sql("show track_sql_count;")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2: 修改track_sql_count为0，重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "track_sql_count=0")
        self.assertTrue(result)
        LOGGER.info("期望：重启后查询结果为off")
        status = COMMONSH.restart_db_cluster()
        self.assertTrue(status)
        sql_cmd = COMMONSH.execut_db_sql("show track_sql_count;")
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2: 修改track_sql_count为false，重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "track_sql_count=false")
        self.assertTrue(result)
        LOGGER.info("期望：重启后查询结果为off")
        status = COMMONSH.restart_db_cluster()
        self.assertTrue(status)
        sql_cmd = COMMONSH.execut_db_sql("show track_sql_count;")
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2: 修改track_sql_count为no，重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "track_sql_count=no")
        self.assertTrue(result)
        LOGGER.info("期望：重启后查询结果为off")
        status = COMMONSH.restart_db_cluster()
        self.assertTrue(status)
        sql_cmd = COMMONSH.execut_db_sql("show track_sql_count;")
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤3: 恢复默认值")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "track_sql_count=on")
        self.assertTrue(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show track_sql_count;")
        if "on" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                   "track_sql_count=on")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0077执行结束==")
