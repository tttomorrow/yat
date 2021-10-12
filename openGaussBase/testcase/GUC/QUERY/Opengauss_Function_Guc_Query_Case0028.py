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
Case Name   : 主机+备机分别设置淘汰比例0.2和0
Description :
    1、主备查询参数默认值；
    show enable_auto_clean_unique_sql;
    show enable_resource_track;
    show instr_unique_sql_count;
    show unique_sql_clean_ratio;
    2、主机修改unique_sql_clean_ratio为0.2，备机修改unique_sql_clean_ratio为0
    重启使其生效，并校验其预期结果
    gs_guc set -D {dn1} -c "enable_auto_clean_unique_sql=on"
    gs_guc set -D {dn1} -c "unique_sql_clean_ratio=0.2"
    gs_guc set -D {dn1} -c "unique_sql_clean_ratio=0"
    gs_om -t stop && gs_om -t start
    show unique_sql_clean_ratio;
    3、清空记录，执行10+1 unique_sql，触发自动淘汰，查看主备hash table记录条数
    select reset_unique_sql('GLOBAL','ALL',100);
    select count(va) from (select get_instr_unique_sql() as va);
    gsql -r -d -p -f test.sql
    select count(va) from (select get_instr_unique_sql() as va);
    4、备机修改unique_sql_clean_ratio为0.2，主机修改unique_sql_clean_ratio为0，
    重启使其生效，并校验其预期结果；
    gs_guc set -D {dn1} -c "unique_sql_clean_ratio=0.2"
    gs_guc set -D {dn1} -c "unique_sql_clean_ratio=0"
    gs_om -t stop && gs_om -t start
    show unique_sql_clean_ratio;
    5、清空记录，执行10+1 unique_sql，触发自动淘汰，查看主备hash table记录条数
    select reset_unique_sql('GLOBAL','ALL',100);
    select count(va) from (select get_instr_unique_sql() as va);
    gsql -r -d -p -f test.sql
    select count(va) from (select get_instr_unique_sql() as va);
    6、恢复默认值；
    gs_guc set -N all -I all -c "enable_auto_clean_unique_sql=off"
    gs_guc set -N all -I all -c "unique_sql_clean_ratio=0"
    gs_om -t stop && gs_om -t start
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数
    3、主机查看hash table记录条数为81，备机为100
    4、参数修改成功，校验修改后系统参数
    5、备机查看hash table记录条数为81，主机为100
    6、恢复默认值成功；
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
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0028 start==")
        self.constant = Constant()
        self.com_s1 = CommonSH("Standby1DbUser")
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
        LOGGER.info("主机设置")
        self.set_gs_guc("enable_auto_clean_unique_sql", "yes")
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        self.set_gs_guc("use_workload_manager", "on", "reload")
        self.set_gs_guc("enable_resource_track", "on", "reload")
        self.set_gs_guc("instr_unique_sql_count", "50", "reload")
        self.set_gs_guc("unique_sql_clean_ratio", "0.1", "reload")
        sql_cmd = COMMONSH.execut_db_sql("show enable_resource_track;"
                                         "show unique_sql_clean_ratio;"
                                         "show use_workload_manager;"
                                         "show instr_unique_sql_count;"
                                         "show enable_auto_clean_unique_sql;")
        LOGGER.info(sql_cmd)
        self.assertNotIn("off", sql_cmd)
        self.assertIn("on", sql_cmd)
        self.assertIn("50", sql_cmd)
        self.assertIn("0.1", sql_cmd)

        LOGGER.info("备1设置")
        result = self.com_s1.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"unique_sql_clean_ratio=0.2",
                                           single=True)
        LOGGER.info(result)
        sql_cmd = COMMONSH.execut_db_sql("show unique_sql_clean_ratio")
        LOGGER.info(sql_cmd)
        self.assertIn("0.1", sql_cmd)
        sql_cmd = self.com_s1.execut_db_sql("show unique_sql_clean_ratio")
        LOGGER.info(sql_cmd)
        self.assertIn("0.2", sql_cmd)

        LOGGER.info("步骤3：清空记录，主机执行100+1 unique_sql，"
                    "备机执行20+1 unique_sql触发自动淘汰，查看hash table记录条数")
        com_list = [COMMONSH, self.com_s1]
        for com in com_list:
            result = com.execut_db_sql("select "
                "reset_unique_sql('GLOBAL','ALL',100);"
                "select count(*) from dbe_perf.statement;")
            LOGGER.info(result)
            self.assertIn("t\n", result)
            self.assertIn("1\n", result)
            table_list = ["GS_MATVIEW", "PG_AM", "PG_AMOP", "PG_AMPROC",
                          "PG_ATTRDEF", "PG_ATTRIBUTE", "PG_AUTHID",
                          "PG_AUTH_HISTORY", "PG_AUTH_MEMBERS", "PG_CAST",
                          "PG_CLASS", "PG_COLLATION", "PG_CONSTRAINT",
                          "PG_CONVERSION", "PG_DATABASE", "PG_DEFAULT_ACL",
                          "PG_DEPEND", "PG_DESCRIPTION", "PG_DIRECTORY",
                          "PG_ENUM", "PG_EXTENSION", "PG_INDEX",
                          "PG_INHERITS", "PG_JOB", "PG_JOB_PROC",
                          "PG_LANGUAGE", "PG_LARGEOBJECT", "PG_OPERATOR",
                          "PG_OPFAMILY", "PG_PARTITION", "PG_PLTEMPLATE",
                          "PG_PROC", "PG_RANGE", "PG_RESOURCE_POOL",
                          "PG_REWRITE", "PG_RLSPOLICY", "PG_SECLABEL",
                          "PG_SHDEPEND", "PG_SHDESCRIPTION", "PG_SHSECLABEL",
                          "PG_STATISTIC", "PG_STATISTIC_EXT",
                          "PG_TABLESPACE", "PG_TRIGGER", "PG_TS_CONFIG",
                          "PG_TS_PARSER"]
            for table in table_list:
                result = com.execut_db_sql(f"select count(*) from {table}")
                LOGGER.info(result)
                self.assertNotIn("ERROR", result)
            result = com.execut_db_sql("select count(*) "
                "from dbe_perf.statement;")
            LOGGER.info(result)
            self.assertIn("50\n", result)
        result = COMMONSH.execut_db_sql("select count(va) "
            "from (select get_instr_unique_sql() as va);")
        LOGGER.info(result)
        self.assertIn("46\n", result)
        result = self.com_s1.execut_db_sql("select count(va) "
            "from (select get_instr_unique_sql() as va);")
        LOGGER.info(result)
        self.assertIn("41\n", result)

    def tearDown(self):
        LOGGER.info("步骤4：恢复默认值")
        self.set_gs_guc("enable_auto_clean_unique_sql", "no")
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        self.set_gs_guc("unique_sql_clean_ratio", "0.1", "reload")
        self.set_gs_guc("instr_unique_sql_count", "100", "reload")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0028 finish=")
