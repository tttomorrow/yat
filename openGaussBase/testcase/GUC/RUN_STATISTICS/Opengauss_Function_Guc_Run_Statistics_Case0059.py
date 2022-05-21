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
Case Name   : 修改参数stats_temp_directory设置为汉字
Description :
    步骤1:查询stats_temp_directory默认值
    show stats_temp_directory;
    步骤2:修改参数stats_temp_directory设置为汉字
    gs_guc reload -N all -D {CLUSTER/DN1} -c "stats_temp_directory=地址";
    show stats_temp_directory;
    步骤3:恢复默认值
    gs_guc reload -D {CLUSTER/DN1} -c "stats_temp_directory=pg_stat_tmp";
Expect      :
    步骤1:显示默认值pg_stat_tmp
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
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0059"
                    "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_guc(self):
        LOGGER.info("步骤1:查询stats_temp_directory 期望：默认值pg_stat_tmp")
        sql_cmd = COMMONSH.execut_db_sql("show stats_temp_directory;")
        LOGGER.info(sql_cmd)
        self.assertEqual("pg_stat_tmp", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:修改为' '，重启，期望：设置成功")
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "stats_temp_directory="
                                        "地址")
        self.assertFalse(result)

        LOGGER.info("期望：重启后查询结果为pg_stat_tmp")
        status = COMMONSH.restart_db_cluster()
        self.assertTrue(status)
        sql_cmd = COMMONSH.execut_db_sql("show stats_temp_directory;")
        LOGGER.info(sql_cmd)
        self.assertEqual("pg_stat_tmp",
                         sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤3:恢复默认值")
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "stats_temp_directory="
                                        "'pg_stat_tmp'")
        self.assertTrue(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show stats_temp_directory;")
        if "pg_stat_tmp" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                   "stats_temp_directory='pg_stat_tmp'")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0059"
                    "执行结束==")
