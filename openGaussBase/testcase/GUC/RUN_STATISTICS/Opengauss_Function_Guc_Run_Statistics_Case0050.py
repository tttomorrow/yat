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
Case Name   : 方式三修改参数track_activity_query_size为2048,设置失败不生效
Description :
    1.查询默认值
    show track_activity_query_size;
    2.方式三修改参数track_activity_query_size为2048
    source env
    alter database dbname set track_activity_query_size to 2048;
    ALTER USER username set track_activity_query_size to 2048;
    set track_activity_query_size to 2048;
    show track_activity_query_size;
    3.恢复默认值
Expect      :
    1.默认值显示为1024
    2.设置失败不生效,查询为1024
    3.恢复默认值
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class Guctestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0050"
            "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.user_node = Node("PrimaryDbUser")

    def test_guc(self):
        LOGGER.info("步骤1:查询track_function默认值 期望：默认值1024")
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("1024", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:方式三修改track_function为2048，重启 设置失败")
        result = COMMONSH.execut_db_sql("alter database postgres "
            "set track_activity_query_size to 2048;")
        self.assertIn("ERROR", result)
        LOGGER.info("期望：查询结果为1024")
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        self.assertIn("1024\n", sql_cmd)

        result = COMMONSH.execut_db_sql(f"alter user {self.user_node.db_user} "
            f"set track_activity_query_size to 2048;")
        self.assertIn("ERROR", result)
        LOGGER.info("期望：查询结果为1024")

        result = COMMONSH.execut_db_sql("set track_activity_query_size "
                                      "to 2048;")
        self.assertIn("ERROR", result)
        LOGGER.info("期望：查询结果为1024")
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        self.assertIn("1024\n", sql_cmd)

        LOGGER.info("步骤3:恢复默认值")
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_activity_query_size=1024")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        if "1024" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  "track_activity_query_size=1024")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0050"
            "执行结束==")
