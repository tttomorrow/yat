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
Case Name   : 
Description :
            1、查看IsInplaceUpgrade默认值；
            show IsInplaceUpgrade;
            2、修改IsInplaceUpgrade为'test'、123456等，校验其预期结果；
            gs_guc set -D {cluster/dn1} -c "IsInplaceUpgrade='test'";
            gs_guc set -D {cluster/dn1} -c "IsInplaceUpgrade=123456";
            3、恢复默认值；
Expect      :
            1、显示默认值；
            2、参数修改失败，预期结果正常；
            3、恢复默认值；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class Guctestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("Opengauss_Function_Guc_Upgrade_Case0002开始执行")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("查询IsInplaceUpgrade 期望：默认值off")
        sql_cmd = COMMONSH.execut_db_sql("show IsInplaceUpgrade;")
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("修改IsInplaceUpgrade为'test' 期望设置失败")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "IsInplaceUpgrade='test'")
        self.assertFalse(result)

        LOGGER.info("修改IsInplaceUpgrade为123456 期望设置失败")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "IsInplaceUpgrade=123456")
        self.assertFalse(result)

        LOGGER.info("期望：重启后查询结果为off")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql("show IsInplaceUpgrade;")
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.split("\n")[-2].strip())

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show IsInplaceUpgrade;")
        if "off" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  "IsInplaceUpgrade=off")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        sql_cmd = COMMONSH.execut_db_sql("show IsInplaceUpgrade;")
        LOGGER.info(sql_cmd)
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.assertEqual("off", sql_cmd.split("\n")[-2].strip())
        LOGGER.info("Opengauss_Function_Guc_Upgrade_Case0002执行结束")
