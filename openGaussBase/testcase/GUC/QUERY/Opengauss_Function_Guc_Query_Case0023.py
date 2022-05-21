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
Case Name   : instr_unique_sql_count大改小后 触发自动淘汰
Description :
    1、查询参数默认值；
    show enable_auto_clean_unique_sql;
    show use_workload_manager;
    show enable_resource_track;
    show instr_unique_sql_count;
    2、enable_auto_clean_unique_sql为on，重启使其生效，并校验其预期结果；
    gs_guc set -N all -I all -c "enable_auto_clean_unique_sql=on"
    gs_om -t stop && gs_om -t start
    3、清空hsah table，执行50 unique_sql，查看hash table记录条数
    select reset_unique_sql('GLOBAL','ALL',100);
    select count(va) from (select get_instr_unique_sql() as va);
    gsql -r -d -p -f test.sql
    select count(va) from (select get_instr_unique_sql() as va);
    4、修改参数instr_unique_sql_count为50 查看记录条数
    gs_guc reload -N all -I all -c "instr_unique_sql_count=50"
    show instr_unique_sql_count;
    select count(va) from (select get_instr_unique_sql() as va);
    5、执行unique_sql 49+1条 触发自动淘汰 查看记录条数
    gsql -r -d -p -f test.sql
    gsql -r -d -p -c "select 1;"
    select count(va) from (select get_instr_unique_sql() as va);
    6、恢复默认值；
    gs_guc set -N all -I all -c "enable_auto_clean_unique_sql=off"
    gs_guc set -N all -I all -c "instr_unique_sql_count=100"
    gs_om -t stop && gs_om -t start
Expect      :
    1、显示默认值；
    2、参数修改成功
    3、查看hash table记录条数为50
    4、修改成功 查询为50 记录条数为1
    5、执行成功 触发自动淘汰 查看hash table记录条数为46
    6、恢复默认值成功；
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
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0023 start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

    def set_gs_guc(self, param, value, method="set"):
        sql_cmd = COMMONSH.execut_db_sql(f"show {param}")
        LOGGER.info(sql_cmd)
        if f"{value}" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc(method,
                                   self.constant.GSGUC_SUCCESS_MSG,
                                   f"{param}={value}")
        LOGGER.info(f"{param} is {value}")

    def test_unique_sql(self):
        LOGGER.info("步骤1+2：核对参数默认值 并修改参数")
        self.set_gs_guc("enable_auto_clean_unique_sql", "true")
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)

        self.set_gs_guc("use_workload_manager", "on", "reload")
        self.set_gs_guc("enable_resource_track", "on", "reload")
        self.set_gs_guc("instr_unique_sql_count", "100", "reload")
        sql_cmd = COMMONSH.execut_db_sql("show enable_resource_track;"
                                         "show use_workload_manager;"
                                         "show instr_unique_sql_count;"
                                         "show enable_auto_clean_unique_sql;")
        LOGGER.info(sql_cmd)
        self.assertNotIn("off", sql_cmd)
        self.assertIn("on", sql_cmd)
        self.assertIn("100", sql_cmd)

        LOGGER.info("步骤3：清空记录后unique sql")
        result = COMMONSH.execut_db_sql("select "
            "reset_unique_sql('GLOBAL','ALL',100);"
            "select count(*) from dbe_perf.statement;")
        LOGGER.info(result)
        self.assertIn("t\n", result)
        for j in range(48):
            tablename = f"unique_table_{j}"
            result = COMMONSH.execut_db_sql(f"drop table "
                f"if exists {tablename};"
                f"create table {tablename}(a int, b int);"
                f"drop table if exists {tablename};")
            LOGGER.info(result)
            self.assertNotIn("ERROR", result)
        result = COMMONSH.execut_db_sql("select count(*) from "
            "dbe_perf.statement;")
        self.assertIn("100\n", result)

        LOGGER.info(f"步骤4：修改参数instr_unique_sql_count为50 查看记录条数")
        self.set_gs_guc("instr_unique_sql_count", "50", "reload")
        sql_cmd = COMMONSH.execut_db_sql("show instr_unique_sql_count;")
        LOGGER.info(sql_cmd)
        self.assertTrue("50", sql_cmd.splitlines()[-2].strip())
        result = COMMONSH.execut_db_sql("select count(*) "
            "from dbe_perf.statement;")
        LOGGER.info(result)
        self.assertIn("5\n", result)

        LOGGER.info("步骤5: 执行unique_sql 49+1条 触发自动淘汰 查看记录条数")
        for j in range(49, 71):
            tablename = f"unique_table_{j}"
            result = COMMONSH.execut_db_sql(f"drop table "
                f"if exists {tablename};"
                f"create table {tablename}(a int, b int);"
                f"drop table if exists {tablename};")
            LOGGER.info(result)
            self.assertNotIn("ERROR", result)
        result = COMMONSH.execut_db_sql("select count(*) "
            "from dbe_perf.statement limit 1;")
        LOGGER.info(result)
        self.assertIn("50\n", result)

        result = COMMONSH.execut_db_sql("select count(va) "
            "from (select get_instr_unique_sql() as va);")
        LOGGER.info(result)
        self.assertIn("46\n", result)

    def tearDown(self):
        LOGGER.info("步骤6：恢复默认值")
        self.set_gs_guc("enable_auto_clean_unique_sql", "false")
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0023 finish=")
