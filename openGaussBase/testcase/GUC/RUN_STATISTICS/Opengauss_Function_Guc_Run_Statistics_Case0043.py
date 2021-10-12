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
Case Name   : 修改参数track_io_timing设置为空浮点数字母NULL等,合理报错不生效
Description :
    1、查询track_io_timing默认值
    show track_io_timing;
    2、修改参数track_io_timing设置为空 浮点数 字母 NULL等
    show track_io_timing;
    3、恢复默认值
Expect      :
    1、显示默认值off
    2、合理报错不生效
    3、恢复默认值成功
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
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0043"
                    "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("1、查询track_io_timing 期望：默认值off")
        sql_cmd = COMMONSH.execut_db_sql("show track_io_timing;")
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("2、修改参数track_io_timing设置为空浮点数字母NULL等")
        temp_list = ["''", "' '", 3.2, 'aa', 'NULL']
        for i in temp_list:
            result = COMMONSH.execute_gsguc("set",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"track_io_timing={i}")
            self.assertFalse(result)
            result = COMMONSH.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"track_activities={i}")
            self.assertFalse(result)

        LOGGER.info("3、恢复默认值")
        del temp_list
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_io_timing=off")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show track_io_timing;")
        if "off" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  "track_io_timing=off")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0043"
                    "执行结束==")
