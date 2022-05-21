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
Case Name   : 修改transaction_isolation为repeatable read，观察其预期结果
Description :
            1、查询transaction_isolation默认值；
            show transaction_isolation；
            2、修改transaction_isolation为repeatable read，重启
            gs_guc set -D {cluster/dn1}
            -c "transaction_isolation='repeatable read'"
            3、恢复默认值；
Expect      :
            1、显示默认值；
            2、修改成功 重启成功 但不生效 不支持set修改 预期结果正常
            3、恢复默认值成功；
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
        LOGGER.info("==Opengauss_Function_Guc_Opengauss_Transaction"
                    "_Case0001开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("查询transaction_isolation 默认值'read committed'")
        sql_cmd = COMMONSH.execut_db_sql("show transaction_isolation;")
        LOGGER.info(sql_cmd)
        self.assertEqual("read committed", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("修改为'repeatable read'重启生效，期望设置失败")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "transaction_isolation"
                                       "='repeatable read'")
        self.assertTrue(result)

        LOGGER.info("期望：重启后查询结果为repeatable read")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql("show transaction_isolation;")
        LOGGER.info(sql_cmd)
        self.assertEqual("read committed", sql_cmd.split("\n")[-2].strip())

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show transaction_isolation;")
        LOGGER.info(sql_cmd)
        if "read committed" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  "transaction_isolation="
                                  "'read committed'")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        sql_cmd = COMMONSH.execut_db_sql("show transaction_isolation;")
        LOGGER.info(sql_cmd)
        self.assertEqual("read committed", sql_cmd.split("\n")[-2].strip())
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Opengauss_Transaction"
                    "_Case0001执行结束==")
