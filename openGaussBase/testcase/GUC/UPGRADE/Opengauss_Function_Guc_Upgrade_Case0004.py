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
            1、查看{self.arg_name}默认值；
            show {self.arg_name};
            2、修改{self.arg_name}为'test'、123456、
            false等，校验其预期结果；
            gs_guc set -D {cluster/dn1}
            -c "{self.arg_name}='test'";
            gs_guc set -D {cluster/dn1}
            -c "{self.arg_name}=123456";
            gs_guc set -D {cluster/dn1}
            -c "{self.arg_name}=false";
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
        LOGGER.info("Opengauss_Function_Guc_Upgrade_Case0004开始执行")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.arg_name = "inplace_upgrade_next_system_object_oids"

    def test_guc(self):
        LOGGER.info("查询{self.arg_name} 期望：默认值")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.arg_name};")
        LOGGER.info(sql_cmd)
        self.assertEqual("", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("改{self.arg_name}为'test'期望设置失败")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"{self.arg_name}='test'")
        self.assertFalse(result)

        LOGGER.info("改{self.arg_name}为123456期望设置失败")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"{self.arg_name}=123456")
        self.assertFalse(result)

        LOGGER.info("修改{self.arg_name}为false期望设置失败")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"{self.arg_name}=false")
        self.assertFalse(result)

        LOGGER.info("期望：重启后查询结果为")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.arg_name};")
        LOGGER.info(sql_cmd)
        self.assertEqual("", sql_cmd.split("\n")[-2].strip())

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.arg_name};")
        if "" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                   f"{self.arg_name}=''")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.arg_name};")
        LOGGER.info(sql_cmd)
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.assertEqual("", sql_cmd.split("\n")[-2].strip())
        LOGGER.info("Opengauss_Function_Guc_Upgrade_Case0004执行结束")
