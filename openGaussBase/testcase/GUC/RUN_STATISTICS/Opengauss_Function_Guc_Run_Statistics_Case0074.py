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
Case Name   : 方式四修改参数track_sql_count为off
Description :
    步骤1:查询track_sql_count默认值
    show track_sql_count;
    步骤2:方式四修改参数track_sql_count为off
    alter system set track_sql_count to off;
    show track_sql_count;
    步骤3:恢复默认值
    alter system set track_sql_count to on;
Expect      :
    步骤1:显示默认值on
    步骤2:参数设置失败合理报错，校验参数值为on
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
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0074开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("步骤1:查询track_sql_count 期望：默认值on")
        sql_cmd = COMMONSH.execut_db_sql("show track_sql_count;")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:方式四修改参数track_sql_count为off")
        sql_cmd = COMMONSH.execut_db_sql("alter system set "
                                       "track_sql_count to off;"
                                       "show track_sql_count;")
        self.assertIn("ERROR", sql_cmd)
        self.assertIn("on\n", sql_cmd)

        LOGGER.info("步骤3:恢复默认值")
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_sql_count=on")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show track_sql_count;")
        if "on" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  "track_sql_count=on")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0074执行结束==")
