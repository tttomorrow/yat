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
Case Name   : 核对自动淘汰日志
Description :
    1、查询参数默认值；
    2、设置参数,打开日志记录，重启使其生效，并校验其预期结果
    3、清空记录，执行100+1 unique_sql,查看hash表记录条数并核对，日志
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数
    3、查看hash table记录条数为0，日志记录自动淘汰
    4、恢复默认值成功；
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class GucTestCase(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("==Opengauss_Function_Guc_Query_Case0048 start==")
        self.constant = Constant()
        self.com = CommonSH("PrimaryDbUser")
        self.common = Common()
        self.user_node = Node("PrimaryDbUser")

        status = self.com.get_db_cluster_status("detail")
        self.log.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

        self.log_path = os.path.join(macro.PG_LOG_PATH,
                                     macro.DN_NODE_NAME.split('/')[0])
        self.log.info(self.log_path)

        text = "备份postgresql.conf文件"
        self.log.info(text)
        self.file = os.path.join(macro.DB_INSTANCE_PATH,
                                 macro.DB_PG_CONFIG_NAME)
        result = self.common.get_sh_result(self.user_node,
                                           f"cp {self.file} "
                                           f"{self.file}backup")
        self.log.info(result)

    def test_guc_query(self):
        text = "--step1:查询参数默认值; expect:成功"
        self.log.info(text)
        self.log_min_messages = self.common.show_param("log_min_messages")
        self.log.info(self.log_min_messages)
        self.logging_module = self.common.show_param("logging_module")
        self.log.info(self.logging_module)

        text = "--step1:修改参数并重启; expect:成功"
        self.log.info(text)
        param_list = ["enable_resource_track=on",
                      "enable_auto_clean_unique_sql=on",
                      "log_min_messages=log",
                      "logging_module='on(ALL)'"]
        for param in param_list:
            res = self.com.execute_gsguc("set",
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         param)
            self.log.info(res)
            self.assertTrue(res)
        status = self.com.restart_db_cluster()
        self.log.info(status)
        sql_cmd = self.com.execut_db_sql("show enable_resource_track;"
                                         "show log_min_messages;"
                                         "show logging_module;"
                                         "show enable_auto_clean_unique_sql;")
        self.log.info(sql_cmd)
        self.assertIn("on", sql_cmd, "执行失败:" + text)
        self.assertIn("log\n", sql_cmd, "执行失败:" + text)
        self.assertIn("ALL,on(", sql_cmd, "执行失败:" + text)
        self.assertIn("off()", sql_cmd, "执行失败:" + text)

        text = "--step3:清空记录，执行100+1 unique_sql,查看hash表记录条数并核对日志; expect:成功"
        self.log.info(text)
        result = self.com.execut_db_sql("select "
            "reset_unique_sql('global','all',100);"
            "select count(*) from dbe_perf.statement;")
        self.log.info(result)
        self.assertIn("t\n", result, "执行失败:" + text)
        self.assertIn("1\n", result, "执行失败:" + text)
        for j in range(46):
            tablename = f"unique_table_{j}"
            result = self.com.execut_db_sql(f"drop table "
                f"if exists {tablename};"
                f"create table {tablename}(a int, b int);"
                f"drop table if exists {tablename};")
            self.log.info(result)
            self.assertNotIn("ERROR", result, "执行失败:" + text)

        sql = "select count(*) from dbe_perf.statement;"
        result = self.com.execut_db_sql(sql)
        self.log.info(result)
        num = result.splitlines()[-2].strip()
        table_list = ["pg_extension", "pg_index", "pg_inherits",
                      "pg_class", "pg_proc", "pg_cast", "pg_object",
                      "pg_type", "pg_operator", "pg_synonym", "pg_ts_dict"]
        for i in range(100 - int(num)):
            sql = f"select count(*) from {table_list[i]}"
            res = self.com.execut_db_sql(sql)
            self.assertNotIn("ERROR", res)

        result = self.com.execut_db_sql("select count(*) "
                                        "from dbe_perf.statement;")
        self.log.info(result)
        self.assertIn("100\n", result, "执行失败:" + text)

        self.log.info("查询当前[UniqueSQL] Auto-cleanup数量")
        sql = f"cat {self.log_path}/* | grep 'Auto-cleanup over'"
        self.log.info(sql)
        result = self.common.get_sh_result(self.user_node, sql)
        self.log.info(result)
        self.assertNotIn("bash", result)
        self.assertNotIn("ERROR", result)
        num_before = result.count("UniqueSQL")

        self.log.info("触发自动淘汰")
        result = self.com.execut_db_sql("select count(va) "
            "from (select get_instr_unique_sql() as va);")
        self.log.info(result)
        self.assertIn("91\n", result)

        self.log.info("查询触发自动淘汰后[UniqueSQL] Auto-cleanup数量")
        result = self.common.get_sh_result(self.user_node, sql)
        self.log.info(result)
        self.assertNotIn("bash", result)
        self.assertNotIn("ERROR", result)
        num_alter = result.count("UniqueSQL")
        self.log.info("核对触发自动淘汰后日志打印Auto-cleanup")
        self.assertGreater(num_alter, num_before)

    def tearDown(self):
        text = "--step4:清理环境; expect:成功"
        self.log.info(text)
        self.log.info("恢复postgresql.conf文件")
        mv_result = self.common.get_sh_result(self.user_node,
                                           f"mv {self.file}backup "
                                           f"{self.file}")
        self.log.info(mv_result)

        status = self.com.restart_db_cluster()
        self.log.info(status)
        status = self.com.get_db_cluster_status("detail")
        self.log.info(status)

        result = self.com.execut_db_sql("show enable_resource_track;"
                                        "show log_min_messages;"
                                        "show logging_module;"
                                        "show enable_auto_clean_unique_sql;")
        self.log.info(result)

        self.assertIn("on", result, "执行失败:" + text)
        self.assertIn("off", result, "执行失败:" + text)
        self.assertIn(f"{self.logging_module}", result, "执行失败:" + text)
        self.assertIn(f"{self.log_min_messages}", result, "执行失败:" + text)
        self.assertEqual("", mv_result, "执行失败:" + text)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info("==Opengauss_Function_Guc_Query_Case0048 finish=")
