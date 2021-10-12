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
Case Name   : 修改参数modify_initial_password为其他数据类型及超边界值，并校验其预期结果。
Description :
    1、查看modify_initial_password默认值 期望：off
    show modify_initial_password;
    2、修改modify_initial_password为abc等，期望：合理报错
    gs_guc reload -D {cluster/dn1} -c "modify_initial_password='abc'";
    gs_guc reload -D {cluster/dn1} -c "modify_initial_password=-1";
    gs_guc reload -D {cluster/dn1} -c "modify_initial_password=3.569";
    gs_guc reload -D {cluster/dn1} -c "modify_initial_password=''";
    gs_guc reload -D {cluster/dn1} -c "modify_initial_password=' '";
    gs_guc reload -D {cluster/dn1} -c "modify_initial_password=null";
    3、恢复默认值 无需恢复
Expect      :
    1、查看modify_initial_password默认值 期望：off
    2、修改modify_initial_password为abc等，期望：合理报错
    3、恢复默认值 无需恢复
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
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0224"
            " start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_guc(self):
        LOGGER.info("步骤1：查询modify_initial_password 期望：默认值off")
        sql_cmd = COMMONSH.execut_db_sql("show modify_initial_password;")
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("步骤2:修改modify_initial_password为abc等，期望：修改失败，show参数为默认值")
        tar_list = ["'abc'", -1, 3.569, "''", "' '", "null"]
        for i in tar_list:
            result = COMMONSH.execute_gsguc("reload",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"modify_initial_password={i}")
            self.assertFalse(result)
            sql_cmd = COMMONSH.execut_db_sql("show modify_initial_password;")
            LOGGER.info(sql_cmd)
            self.assertEqual("off", sql_cmd.split("\n")[-2].strip())

    def tearDown(self):
        LOGGER.info("步骤3:恢复默认值")
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "modify_initial_password=off")
        LOGGER.info(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0224"
            " finish==")
