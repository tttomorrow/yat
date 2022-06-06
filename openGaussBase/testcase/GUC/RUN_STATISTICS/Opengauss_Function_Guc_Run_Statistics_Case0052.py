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
Case Name   : 修改参数track_activity_query_size为单位KB/MB/GB,设置失败
Description :
    步骤1:查询track_activity_query_size默认值
    show track_activity_query_size;
    步骤2:修改track_activity_query_size为2048KB/1024MB/2GB，重启 并校验其预期结果
    gs_guc set -D {cluster/dn1} -c "track_activity_query_size=2048KB"
    gs_om -t stop && gs_om -t start
    show track_activity_query_size;
    gs_guc set -D {cluster/dn1} -c "track_activity_query_size=1024MB"
    gs_om -t stop && gs_om -t start
    show track_activity_query_size;
    gs_guc set -D {cluster/dn1} -c "track_activity_query_size=2GB"
    gs_om -t stop && gs_om -t start
    show track_activity_query_size;
    步骤3:恢复默认值
Expect      :
    步骤1:显示默认值1024
    步骤2:参数修改成功，查询为修改值
    步骤3:恢复默认值成功
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
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0052"
            "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("步骤1:查询track_activity_query_size 期望：默认值1024")
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("1024", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:方式一修改track_activity_query_size为'2048KB'")
        result = COMMONSH.execute_gsguc("set",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_activity_query_size='2048KB'")
        self.assertFalse(result)
        COMMONSH.restart_db_cluster()
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("1024", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("方式一修改参数track_activity_query_size为'1024MB'")
        result = COMMONSH.execute_gsguc("set",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_activity_query_size='1024MB'")
        self.assertFalse(result)
        COMMONSH.restart_db_cluster()
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("1024", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("方式一修改参数track_activity_query_size为'2GB'")
        result = COMMONSH.execute_gsguc("set",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_activity_query_size='2GB'")
        self.assertFalse(result)
        COMMONSH.restart_db_cluster()
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("1024", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤3:恢复默认值")
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_activity_query_size=1024")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        if "1024" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  "track_activity_query_size=1024")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0052"
            "执行结束==")
