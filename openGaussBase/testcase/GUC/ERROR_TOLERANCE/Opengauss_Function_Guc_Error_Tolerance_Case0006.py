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
Case Name   : 修改max_query_retry_times为其他数据类型，观察其预期结果；
Description :
            1、查询max_query_retry_times默认值；
            show max_query_retry_times；
            2、修改max_query_retry_times为4，观察预期结果；
            set max_query_retry_times to 4;
            3、恢复默认值
Expect      :
            1、显示默认值0；
            2、修改max_query_retry_times成功，预期结果正常；
            3、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GucTest(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Error_Tolerance_Case0006"
                    "开始执行==")
        self.constant = Constant()

        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("==查询max_query_retry_times 期望：默认值0==")
        sql_cmd = COMMONSH.execut_db_sql("show max_query_retry_times;")
        LOGGER.info(sql_cmd)
        self.assertEqual("0", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("==修改max_query_retry_times为4期望合理报错==")
        LOGGER.info("==期望：修改失败，show参数为默认值==")
        result = COMMONSH.execut_db_sql("set max_query_retry_times to 4;")
        LOGGER.info(result)
        self.assertIn("SET", result)

        sql_cmd = COMMONSH.execut_db_sql("show max_query_retry_times;")
        LOGGER.info(sql_cmd)
        self.assertEqual("0", sql_cmd.split("\n")[-2].strip())

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show max_query_retry_times;")
        LOGGER.info(sql_cmd)
        if "0" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  "max_query_retry_times='0'")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        sql_cmd = COMMONSH.execut_db_sql("show max_query_retry_times;")
        LOGGER.info(sql_cmd)
        self.assertEqual("0", sql_cmd.split("\n")[-2].strip())
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Error_Tolerance_Case0006"
                    "执行结束==")
