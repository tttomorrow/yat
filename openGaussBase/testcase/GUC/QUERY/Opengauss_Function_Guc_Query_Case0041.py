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
Case Name   : 打开自动淘汰，比例设置为0 查看生效
Description :
    1、查询参数默认值；
    show enable_auto_clean_unique_sql;
    show enable_resource_track;
    show instr_unique_sql_count;
    show unique_sql_clean_ratio;
    2、修改unique_sql_clean_ratio为0.1，重启使其生效，并校验其预期结果；
    gs_guc set -N all -I all -c "enable_auto_clean_unique_sql=on"
    gs_guc set -N all -I all -c "unique_sql_clean_ratio=0"
    gs_om -t stop && gs_om -t start
    show unique_sql_clean_ratio;
    cat postgresql.conf | grep "unique_sql_clean_ratio"
    3、执行100+1 unique_sql，查看hash table记录条数
    select reset_unique_sql('GLOBAL','ALL',100);
    select count(va) from (select get_instr_unique_sql() as va);
    gsql -r -d -p -f test.sql
    select count(va) from (select get_instr_unique_sql() as va);
    4、恢复默认值 清理环境
    gs_guc set -N all -I all -c "enable_auto_clean_unique_sql=off"
    gs_guc set -N all -I all -c "unique_sql_clean_ratio=0"
    gs_om -t stop && gs_om -t start
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数 核对show和grep
    3、执行成功 触发自动淘汰 查询记录条数91
    4、恢复默认值成功
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
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0041 start==")
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
        self.set_gs_guc("enable_auto_clean_unique_sql", "on")
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        self.set_gs_guc("enable_resource_track", "on", "reload")
        self.set_gs_guc("instr_unique_sql_count", "100", "reload")
        self.set_gs_guc("unique_sql_clean_ratio", "0", "reload")
        sql_cmd = COMMONSH.execut_db_sql("show enable_resource_track;"
                                         "show unique_sql_clean_ratio;"
                                         "show instr_unique_sql_count;"
                                         "show enable_auto_clean_unique_sql;")
        LOGGER.info(sql_cmd)
        self.assertNotIn("off", sql_cmd)
        self.assertIn("on", sql_cmd)
        self.assertIn("100", sql_cmd)
        self.assertIn("0.1", sql_cmd)

        LOGGER.info("步骤3：清空记录后触发自动淘汰")
        result = COMMONSH.execut_db_sql("select "
            "reset_unique_sql('GLOBAL','ALL',100);"
            "select count(*) from dbe_perf.statement;")
        LOGGER.info(result)
        self.assertIn("t\n", result)
        for j in range(48):
            tablename = f"unique_table_{j}"
            result = COMMONSH.execut_db_sql(f"drop table if exists "
                f"{tablename};create table {tablename}(a int, b int);"
                f"drop table if exists {tablename};")
            LOGGER.info(result)
            self.assertNotIn("ERROR", result)
        result = COMMONSH.execut_db_sql("select count(*) "
            "from dbe_perf.statement;")
        LOGGER.info(result)
        self.assertIn("100\n", result)

        LOGGER.info(f"执行第101条并触发自动淘汰")
        result = COMMONSH.execut_db_sql("select count(va) "
            "from (select get_instr_unique_sql() as va);")
        LOGGER.info(result)
        self.assertTrue("91\n" in result)

    def tearDown(self):
        LOGGER.info("步骤5：恢复默认值")
        self.set_gs_guc("enable_auto_clean_unique_sql", "off")
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        self.set_gs_guc("unique_sql_clean_ratio", "0.1", "reload")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0041 finish=")
