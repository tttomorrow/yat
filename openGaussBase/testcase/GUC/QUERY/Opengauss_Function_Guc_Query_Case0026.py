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
Case Name   : 不同用户触发自动淘汰
Description :
    1、查询参数默认值；
    show enable_resource_track;
    show instr_unique_sql_count;
    show unique_sql_clean_ratio;
    2、创建用户赋管理员权限
    drop user if exists query_user026;
    create user query_user026 password "{password}";
    3、修改unique_sql_clean_ratio为0.05，重启使其生效，并校验其预期结果；
    gs_guc set -N all -I all -c "enable_auto_clean_unique_sql=on"
    gs_guc set -N all -I all -c "unique_sql_clean_ratio=0.05"
    gs_om -t stop && gs_om -t start
    show unique_sql_clean_ratio;
    4、清空记录，执行100 unique_sql，不触发自动淘汰，查看hash table记录条数
    select reset_unique_sql('GLOBAL','ALL',100);
    select count(va) from (select get_instr_unique_sql() as va);
    gsql -r -d -p -f test.sql
    select count(va) from (select get_instr_unique_sql() as va);
    5、另一用户在4相同的数据库执行1unique_sql 触发自动淘汰 查看hash table记录条数
    select reset_unique_sql('GLOBAL','ALL',100);
    6、恢复默认值；
    gs_guc set -N all -I all -c "enable_auto_clean_unique_sql=off"
    gs_guc set -N all -I all -c "unique_sql_clean_ratio=0"
    gs_om -t stop && gs_om -t start
Expect      :
    1、显示默认值；
    2、创建用户赋管理员权限成功
    3、参数修改成功，校验修改后系统参数值为0.05；
    4、查看hash table记录条数为100
    5、执行成功 触发自动淘汰 2个用户查看hash table记录条数为81
    6、恢复默认值成功；
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
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0026 start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

        self.user_node = Node("PrimaryDbUser")

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
        self.set_gs_guc("enable_auto_clean_unique_sql", "1")
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)

        self.set_gs_guc("use_workload_manager", "on", "reload")
        self.set_gs_guc("enable_resource_track", "on", "reload")
        self.set_gs_guc("instr_unique_sql_count", "100", "reload")
        self.set_gs_guc("unique_sql_clean_ratio", "0.05", "reload")
        sql_cmd = COMMONSH.execut_db_sql("show enable_resource_track;"
                                         "show unique_sql_clean_ratio;"
                                         "show use_workload_manager;"
                                         "show instr_unique_sql_count;"
                                         "show enable_auto_clean_unique_sql;")
        LOGGER.info(sql_cmd)
        self.assertNotIn("off", sql_cmd)
        self.assertIn("on", sql_cmd)
        self.assertIn("100", sql_cmd)
        self.assertIn("0.05", sql_cmd)

        LOGGER.info("步骤2：清空记录后执行unique_sql 100+1条 触发自动淘汰 查看记录条数")
        result = COMMONSH.execut_db_sql(f'''drop owned by unique_user;\
            drop user unique_user;\
            create user unique_user password \\"{macro.COMMON_PASSWD}\\";\
            grant all privileges to unique_user;''')
        LOGGER.info(result)
        self.assertIn("CREATE ROLE", result)
        self.assertIn("ALTER ROLE", result)

        LOGGER.info("步骤4：清空记录后执行unique_sql 100条 触发自动淘汰 查看记录条数")
        result = COMMONSH.execut_db_sql("select "
            "reset_unique_sql('GLOBAL','ALL',100);"
            "select count(*) from dbe_perf.statement;")
        LOGGER.info(result)
        self.assertIn("t\n", result)
        self.assertIn("1\n", result)
        for j in range(48):
            tablename = f"unique_table_{j}"
            result = COMMONSH.execut_db_sql(f"drop table "
                f"if exists {tablename};"
                f"create table {tablename}(a int, b int);"
                f"drop table if exists {tablename};")
            LOGGER.info(result)
            self.assertNotIn("ERROR", result)
        result = COMMONSH.execut_db_sql("select count(*) "
            "from dbe_perf.statement;")
        LOGGER.info(result)
        self.assertIn("100\n", result)

        LOGGER.info("步骤5：清空记录后执行unique_sql +1条 触发自动淘汰 查看记录条数")
        sql_cmd = f'''source {macro.DB_ENV_PATH};\
            gsql -d {self.user_node.db_name} \
            -p {self.user_node.db_port} \
            -U {self.user_node.db_user} \
            -W {macro.COMMON_PASSWD} \
            -c "select 1;select 'test';";'''
        LOGGER.info(sql_cmd)
        result = self.user_node.sh(sql_cmd).result()
        LOGGER.info(result)
        self.assertIn("1\n", result)
        result = COMMONSH.execut_db_sql("select count(*) "
            "from dbe_perf.statement limit 1;")
        LOGGER.info(result)
        self.assertIn("96\n", result)

    def tearDown(self):
        LOGGER.info("步骤6：恢复默认值")
        result = COMMONSH.execut_db_sql("drop owned by unique_user;"
                                        "drop user if exists unique_user;")
        LOGGER.info(result)
        self.set_gs_guc("enable_auto_clean_unique_sql", "0")
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        self.set_gs_guc("unique_sql_clean_ratio", "0.1", "reload")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0026 finish=")
