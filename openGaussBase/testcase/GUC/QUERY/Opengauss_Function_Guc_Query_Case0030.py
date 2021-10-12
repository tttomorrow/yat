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
Case Name   : 主备+级联备分别设置不同最大条目+淘汰比例 触发自动淘汰
Description :
    1、主备查询参数默认值；
    show enable_auto_clean_unique_sql;
    show enable_resource_track;
    show instr_unique_sql_count;
    show unique_sql_clean_ratio;
    2、主机修改unique_sql_clean_ratio为0.05，最大条目100，
    备机修改unique_sql_clean_ratio为0.1，最大条目20，
    级联备修改unique_sql_clean_ratio为0.2，最大条目30，
    重启使其生效，并校验其预期结果
    gs_guc set -D {dn1} -c "enable_auto_clean_unique_sql=on"
    gs_guc set -D {dn1} -c "instr_unique_sql_count=100"
    gs_guc set -D {dn1} -c "unique_sql_clean_ratio=0.05"
    gs_guc set -D {dn1} -c "instr_unique_sql_count=20"
    gs_guc set -D {dn1} -c "unique_sql_clean_ratio=0.1"
    gs_guc set -D {dn1} -c "instr_unique_sql_count=30"
    gs_guc set -D {dn1} -c "unique_sql_clean_ratio=0.2"
    gs_om -t stop && gs_om -t start
    show unique_sql_clean_ratio;
    3、清空记录，主机执行100+1 unique_sql，
    备机执行20+1 unique_sql触发自动淘汰，
    级联备执行30+1 unique_sql触发自动淘汰，
    查看hash table记录条数
    select reset_unique_sql('GLOBAL','ALL',100);
    select count(va) from (select get_instr_unique_sql() as va);
    gsql -r -d -p -f test.sql
    select count(va) from (select get_instr_unique_sql() as va);
    4、恢复默认值；
    gs_guc set -N all -I all -c "enable_auto_clean_unique_sql=off"
    gs_guc set -N all -I all -c "unique_sql_clean_ratio=0.1"
    gs_guc set -N all -I all -c "instr_unique_sql_count=100"
    gs_om -t stop && gs_om -t start
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数
    3、主机查看hash table记录条数为96，备机查看hash table记录条数为19，备机查看hash table记录条数为25
    4、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


@unittest.skipIf(1 == CommonSH("PrimaryDbUser").get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class Guctestcase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH("PrimaryDbUser")
        self.logger.info("==Opengauss_Function_Guc_Query_Case0030 start==")
        self.constant = Constant()
        self.com_s1 = CommonSH("Standby1DbUser")
        self.com_s2 = CommonSH("Standby2DbUser")
        status = self.primary_sh.get_db_cluster_status("detail")
        self.logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        status = self.primary_sh.restart_db_cluster()
        self.logger.info(status)
        text = "核对数据库状态正常"
        self.logger.info(text)
        status = self.primary_sh.get_db_cluster_status("detail")
        self.logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status,
                        "执行失败" + text)

    def set_gs_guc(self, param, value, method="set"):
        sql_cmd = self.primary_sh.execut_db_sql(f"show {param}")
        self.logger.info(sql_cmd)
        if f"{value}" != sql_cmd.splitlines()[-2].strip():
            self.primary_sh.execute_gsguc(method,
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"{param}={value}")
        self.logger.info(f"{param} is {value}")

    def test_unique_sql(self):
        text = "--step1:核对参数默认值;expect:成功"
        self.logger.info(text)
        self.logger.info("主机设置")
        self.set_gs_guc("use_workload_manager", "on", "reload")
        self.set_gs_guc("enable_resource_track", "on", "reload")
        self.set_gs_guc("enable_auto_clean_unique_sql", "yes")
        status = self.primary_sh.restart_db_cluster()
        self.logger.info(status)
        self.logger.info("重启查询记录被清空")
        result = self.primary_sh.execut_db_sql("select count(*) "
                                               "from dbe_perf.statement;")
        self.logger.info(result)
        self.assertIn("7\n", result)
        text = "--step1:以级联备build备2;expect:成功"
        self.logger.info(text)
        result = self.com_s1.execute_gsctl("build",
                                           "server started",
                                           param="-M cascade_standby")
        self.logger.info(result)
        self.assertTrue(result, "执行失败" + text)
        result = self.com_s1.exec_refresh_conf()
        self.logger.info(result)
        self.assertTrue(result, "执行失败" + text)
        status = self.primary_sh.get_db_cluster_status("detail")
        self.logger.info(status)
        self.assertTrue("S Cascade Normal" in status, "执行失败" + text)
        self.assertTrue("cluster_state   : Normal" in status, "执行失败" + text)

        text = "--step2:3节点分别设置淘汰比例和最大条目;expect:成功"
        self.logger.info(text)
        text = "主机设置"
        self.logger.info(text)
        result = self.com_s1.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"instr_unique_sql_count=100")
        self.logger.info(result)
        result = self.com_s1.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"unique_sql_clean_ratio=0.05")
        self.logger.info(result)
        sql = "show enable_resource_track;show unique_sql_clean_ratio;" \
              "show use_workload_manager;show instr_unique_sql_count;" \
              "show enable_auto_clean_unique_sql;"
        sql_cmd = self.primary_sh.execut_db_sql(sql)
        self.logger.info(sql_cmd)
        self.assertNotIn("off", sql_cmd, "执行失败" + text)
        self.assertIn("on", sql_cmd, "执行失败" + text)
        self.assertIn("100", sql_cmd, "执行失败" + text)
        self.assertIn("0.05", sql_cmd, "执行失败" + text)

        text = "级联备-备2设置"
        self.logger.info(text)
        result = self.com_s2.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"instr_unique_sql_count=30",
                                           single=True)
        self.logger.info(result)
        result = self.com_s2.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"unique_sql_clean_ratio=0.2",
                                           single=True)
        self.logger.info(result)
        sql_cmd = self.com_s2.execut_db_sql("show instr_unique_sql_count;"
                                            "show unique_sql_clean_ratio")
        self.logger.info(sql_cmd)
        self.assertIn("30", sql_cmd, "执行失败" + text)
        self.assertIn("0.2", sql_cmd, "执行失败" + text)

        text = "备1设置"
        self.logger.info(text)
        result = self.com_s1.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"instr_unique_sql_count=20",
                                           single=True)
        self.logger.info(result)
        result = self.com_s1.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"unique_sql_clean_ratio=0.1",
                                           single=True)
        self.logger.info(result)
        sql_cmd = self.com_s1.execut_db_sql("show instr_unique_sql_count;"
                                            "show unique_sql_clean_ratio")
        self.logger.info(sql_cmd)
        self.assertIn("20", sql_cmd, "执行失败" + text)
        self.assertIn("0.1", sql_cmd, "执行失败" + text)

        text = "3节点再次查询 核对参数"
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql("show instr_unique_sql_count;"
                                                "show unique_sql_clean_ratio")
        self.logger.info(sql_cmd)
        self.assertIn("100", sql_cmd, "执行失败" + text)
        self.assertIn("0.05", sql_cmd, "执行失败" + text)
        sql_cmd = self.com_s1.execut_db_sql("show instr_unique_sql_count;"
                                            "show unique_sql_clean_ratio")
        self.logger.info(sql_cmd)
        self.assertIn("20", sql_cmd, "执行失败" + text)
        self.assertIn("0.1", sql_cmd, "执行失败" + text)
        sql_cmd = self.com_s2.execut_db_sql("show instr_unique_sql_count;"
                                            "show unique_sql_clean_ratio")
        self.logger.info(sql_cmd)
        self.assertIn("30", sql_cmd, "执行失败" + text)
        self.assertIn("0.2", sql_cmd, "执行失败" + text)

        text = "--step3:清空记录，主机执行100+1 unique_sql，备机执行20+1 unique_sql " \
               "级联备执行30+1 触发自动淘汰，查看hash table记录条数;" \
               "expect:主机96 备1 19 备2-级联备 25"
        self.logger.info(text)
        text = "主机执行并核对"
        self.logger.info(text)
        result = self.primary_sh.execut_db_sql("select "
               "reset_unique_sql('GLOBAL','ALL',100);"
               "select count(*) from dbe_perf.statement;")
        self.logger.info(result)
        self.assertIn("t\n", result, "执行失败" + text)
        self.assertIn("1\n", result, "执行失败" + text)
        for j in range(47):
            tablename = f"t_unique_table_{j}"
            result = self.primary_sh.execut_db_sql(f"drop table "
                f"if exists {tablename};"
                f"create table {tablename}(a int, b int);"
                f"drop table if exists {tablename};")
            self.logger.info(result)
            self.assertNotIn("ERROR", result, "执行失败" + text)

        self.logger.info("unique_sql不足100时补足100")
        result = self.primary_sh.execut_db_sql("select count(*) "
                                               "from dbe_perf.statement;")
        self.logger.info(result)
        num = int(result.splitlines()[-2].strip())
        table_list = ["PG_EXTENSION", "PG_INDEX", "PG_INHERITS", "PG_JOB",
                      "PG_JOB_PROC", "PG_LANGUAGE", "PG_LARGEOBJECT"]
        for i in range(100 - num):
            result = self.primary_sh.execut_db_sql(f"select count(*) "
                                                   f"from {table_list[i]};")
            self.logger.info(result)
        self.logger.info("unique_sql记录条数达到100")
        result = self.primary_sh.execut_db_sql("select count(*) "
                                               "from dbe_perf.statement;")
        self.logger.info(result)
        self.assertIn("100\n", result, "执行失败" + text)
        result = self.primary_sh.execut_db_sql("select count(va) "
            "from (select get_instr_unique_sql() as va);")
        self.logger.info(result)
        self.assertIn("96\n", result, "执行失败" + text)

        text = "备1执行并核对"
        self.logger.info(text)
        result = self.com_s1.execut_db_sql("select "
            "reset_unique_sql('GLOBAL','ALL',20);"
            "select count(*) from dbe_perf.statement;")
        self.logger.info(result)
        self.assertIn("t\n", result, "执行失败" + text)
        self.assertIn("1\n", result, "执行失败" + text)
        table_list = ["PG_EXTENSION", "PG_INDEX", "PG_INHERITS", "PG_JOB",
                      "PG_JOB_PROC", "PG_LANGUAGE", "PG_LARGEOBJECT",
                      "PG_OPERATOR", "PG_OPFAMILY", "PG_PARTITION",
                      "PG_PLTEMPLATE", "PG_PROC", "PG_RANGE",
                      "PG_RESOURCE_POOL", "PG_REWRITE", "PG_RLSPOLICY",
                      "PG_SECLABEL", "PG_SHDEPEND", "PG_ENUM"]
        for table in table_list:
            res = self.com_s1.execut_db_sql(f"select count(*) from {table}")
            self.logger.info(res)
            self.assertNotIn("ERROR", res, "执行失败" + text)
        result = self.com_s1.execut_db_sql("select count(*) "
                                           "from dbe_perf.statement;")
        self.logger.info(result)
        self.assertIn("20\n", result, "执行失败" + text)
        result = self.com_s1.execut_db_sql("select count(va) "
            "from (select get_instr_unique_sql() as va);")
        self.logger.info(result)
        self.assertIn("19\n", result, "执行失败" + text)

        text = "备2-级联备执行并核对"
        self.logger.info(text)
        result = self.com_s2.execut_db_sql("select "
            "reset_unique_sql('GLOBAL','ALL',30);"
            "select count(*) from dbe_perf.statement;")
        self.logger.info(result)
        self.assertIn("t\n", result, "执行失败" + text)
        self.assertIn("1\n", result, "执行失败" + text)
        table_list = ["PG_EXTENSION", "PG_INDEX", "PG_INHERITS", "PG_JOB",
                      "PG_JOB_PROC", "PG_LANGUAGE", "PG_LARGEOBJECT",
                      "PG_OPERATOR", "PG_OPFAMILY", "PG_PARTITION",
                      "PG_PLTEMPLATE", "PG_PROC", "PG_RANGE",
                      "PG_RESOURCE_POOL", "PG_REWRITE", "PG_RLSPOLICY",
                      "PG_SECLABEL", "PG_SHDEPEND", "PG_ENUM",
                      "PG_STATISTIC", "PG_STATISTIC_EXT", "PG_TABLESPACE",
                      "PG_TRIGGER", "PG_TS_CONFIG", "PG_TS_CONFIG_MAP",
                      "PG_TS_DICT"]
        for table in table_list:
            res = self.com_s2.execut_db_sql(f"select count(*) from {table}")
            self.logger.info(res)
            self.assertNotIn("ERROR", res, "执行失败" + text)
        result = self.com_s2.execut_db_sql("select count(*) "
                                           "from dbe_perf.statement;")
        self.logger.info(result)
        self.assertIn("30\n", result, "执行失败" + text)
        result = self.com_s2.execut_db_sql("select count(va) "
            "from (select get_instr_unique_sql() as va);")
        self.logger.info(result)
        self.assertIn("25\n", result, "执行失败" + text)

    def tearDown(self):
        text = "--step4:恢复默认值;expect:成功"
        self.logger.info(text)
        self.logger.info("恢复集群")
        result = self.com_s1.execute_gsctl("build",
                                           "server started",
                                           param="-b full")
        self.logger.info(result)
        result = self.com_s2.execute_gsctl("build",
                                           "server started",
                                           param="-b full")
        self.logger.info(result)
        result = self.primary_sh.exec_refresh_conf()
        self.logger.info(result)

        self.logger.info("删除表")
        for j in range(48):
            tablename = f"t_unique_table_{j}"
            result = self.primary_sh.execut_db_sql(f"drop table "
                                                   f"if exists {tablename}")
            self.logger.info(result)

        self.logger.info("恢复参数")
        self.set_gs_guc("enable_auto_clean_unique_sql", "no")
        status = self.primary_sh.restart_db_cluster()
        self.logger.info(status)
        self.set_gs_guc("unique_sql_clean_ratio", "0.1", "reload")
        self.set_gs_guc("instr_unique_sql_count", "100", "reload")
        status = self.primary_sh.get_db_cluster_status("detail")
        self.logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status,
                        "执行失败" + text)
        self.logger.info("==Opengauss_Function_Guc_Query_Case0030 finish=")
