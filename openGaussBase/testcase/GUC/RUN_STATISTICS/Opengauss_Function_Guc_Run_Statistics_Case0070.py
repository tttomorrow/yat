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
Case Name   : 修改参数enable_save_datachanged_timestamp设置为空 浮点数 字母 NULL等
Description :
    步骤1:查询enable_save_datachanged_timestamp默认值
    show enable_save_datachanged_timestamp;
    步骤2:修改参数enable_save_datachanged_timestamp设置为空 浮点数 字母 NULL等
    gs_guc set -D {CLUSTER/DN1} -c "enable_save_datachanged_timestamp=''";
    gs_guc set -D {CLUSTER/DN1} -c "enable_save_datachanged_timestamp=' '";
    gs_guc reload -D {CLUSTER/DN1} -c "enable_save_datachanged_timestamp=3.2";
    gs_guc reload -D {CLUSTER/DN1} -c "enable_save_datachanged_timestamp=aa";
    gs_guc reload -D {CLUSTER/DN1} -c "enable_save_datachanged_timestamp=
    NULL";
    show enable_save_datachanged_timestamp;
    步骤3:恢复默认值
    gs_guc reload -D {CLUSTER/DN1} -c "enable_save_datachanged_timestamp=on";
Expect      :
    步骤1:显示默认值on
    步骤2:合理报错不生效
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
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0070开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.param = "enable_save_datachanged_timestamp"

    def test_guc(self):
        LOGGER.info("步骤1:查询enable_save_datachanged_timestamp 期望：默认值on")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:修改参数enable_save_datachanged_timestamp设置为空浮点数字母NULL等")
        temp_list = ["''", "' '", 3.2, "'aa'", 'NULL']
        for i in temp_list:
            result = COMMONSH.execute_gsguc("set",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"{self.param}={i}")
            self.assertFalse(result)
            result = COMMONSH.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"{self.param}={i}")
            self.assertFalse(result)

        LOGGER.info("步骤3:恢复默认值")
        del temp_list
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"{self.param}=on")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        if "on" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"{self.param}=on")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0070执行结束==")
