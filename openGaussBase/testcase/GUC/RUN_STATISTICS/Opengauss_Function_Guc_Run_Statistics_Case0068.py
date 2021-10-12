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
Case Name   : 方式三修改参数enable_save_datachanged_timestamp为off
Description :
    1.查询默认值
    show enable_save_datachanged_timestamp;
    2.方式三修改参数enable_save_datachanged_timestamp为off
    alter database dbname set enable_save_datachanged_timestamp to off;
    ALTER USER username set enable_save_datachanged_timestamp to off;
    set enable_save_datachanged_timestamp to off;
    show enable_save_datachanged_timestamp;
    3.执行DML前后last_data_changed不变
    4.恢复默认值 删除表和数据库
Expect      :
    1.默认值显示为on
    2.设置失败不生效,查询为on
    3.执行DML前后last_data_changed不变
    4.恢复默认值 删除表和数据库
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class Guctestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0068开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.user_node = Node("PrimaryDbUser")
        self.db_name = "testdb"
        self.param = "enable_save_datachanged_timestamp"

    def test_guc(self):
        LOGGER.info("步骤1:查询track_function默认值 期望：默认值on")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:方式三修改track_function为off，重启 设置失败")
        result = COMMONSH.execut_db_sql(f"drop database "
            f"if exists {self.db_name};"
            f"create database {self.db_name};"
            f"alter database {self.db_name} set {self.param} to off;")
        self.assertNotIn("ERROR", result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        LOGGER.info("期望：查询结果为on")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        self.assertIn("on\n", sql_cmd)

        LOGGER.info("步骤4 恢复默认值")
        LOGGER.info("删除表和数据库")
        sql_cmd = COMMONSH.execut_db_sql(f"drop database {self.db_name};")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"{self.param}=on")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        COMMONSH.execut_db_sql(f"drop database if exists {self.db_name};")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        if "on" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"{self.param}=on")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0068执行结束==")
