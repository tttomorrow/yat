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
Case Name   : 修改pgxc_node_name为on，观察预期结果；
Description :
    1、查询pgxc_node_name默认值；
    show pgxc_node_name;
    2、修改pgxc_node_name为123456，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "pgxc_node_name=123456"
    gs_om -t stop && gs_om -t start
    show pgxc_node_name;
    3、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改失败，校验修改后系统参数值为self.default_value；
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
                    "_Case0010开始执行==")
        self.constant = Constant()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc(self):
        LOGGER.info("查询pgxc_node_name 期望：默认值self.default_value")
        sql_cmd = COMMONSH.execut_db_sql("show pgxc_node_name;")
        LOGGER.info(sql_cmd)
        self.default_value = sql_cmd.split("\n")[-2].strip()

        LOGGER.info("方式一修改pgxc_node_name为123456"
                    "重启使其生效，期望：设置失败")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "pgxc_node_name=123456")
        self.assertFalse(result)

        sql_cmd = COMMONSH.execut_db_sql("show pgxc_node_name;")
        LOGGER.info(sql_cmd)
        self.assertIn(self.default_value, sql_cmd)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show pgxc_node_name;")
        if f"{self.default_value}" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                   f"pgxc_node_name='{self.default_value}'")
            COMMONSH.restart_db_cluster()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        LOGGER.info("==Opengauss_Function_Guc_Opengauss_Transaction"
                    "_Case0010执行结束==")
