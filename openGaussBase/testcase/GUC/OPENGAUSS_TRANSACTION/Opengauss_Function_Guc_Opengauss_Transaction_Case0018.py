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
Case Name   : 修改replication_type为123456，观察预期结果；
Description :
    1、查询replication_type默认值；
    show replication_type;
    2、修改replication_type为123456，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "replication_type=123456"
    show replication_type;
    3、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改失败，校验修改后系统参数值为1；
    3、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 == COMMONSH.get_node_num(),
    'Single node, and subsequent codes are not executed.')
class Guctestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Opengauss_Transaction"
                    "_Case0018开始执行==")
        self.constant = Constant()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc(self):
        LOGGER.info("步骤1：查询replication_type 期望：默认值1")
        sql_cmd = COMMONSH.execut_db_sql("show replication_type;")
        LOGGER.info(sql_cmd)
        self.assertIn("1", sql_cmd)

        LOGGER.info("步骤2：方式一修改replication_type为123456"
                    "重启使其生效，期望：设置失败")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "replication_type=123456")
        self.assertFalse(result)

        LOGGER.info("步骤3：恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show replication_type;")
        LOGGER.info(sql_cmd)
        self.assertIn("1", sql_cmd)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show replication_type;")
        if "1" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  "replication_type=1")
            COMMONSH.start_db_cluster()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        LOGGER.info("==Opengauss_Function_Guc_Opengauss_Transaction"
                    "_Case0018执行结束==")
