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
Case Name   : unqiue_sql自动淘汰-wdr报告验证
Description :
    1、查询参数默认值；
    2、修改enable_auto_clean_unique_sql为on，重启使其生效，并校验其预期结果；
    3、生成快照s1
    4、执行100+1 unique_sql，查看hash table记录条数
    5、生成快照s2
    6、生成快照s3
    7、快照1+2 生成wdr报告：生成失败
    8、快照1+3 生成wdr报告：生成失败
    9、快照2+3 生成wdr报告：生成成功
    10、恢复默认值 清理环境
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数
    3、快照生成成功
    4、执行成功 触发自动淘汰 查询记录条数小于100
    5、快照生成成功
    6、快照生成成功
    7、wdr报告生成失败 合理报错
    8、wdr报告生成失败 合理报错
    9、wdr报告生成成功
    10、恢复默认值成功
History     :
"""
import os
import time
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
        self.log.info("==Opengauss_Function_Guc_Query_Case0040 start==")
        self.constant = Constant()
        self.common = Common()
        self.com = CommonSH("PrimaryDbUser")
        self.user_node = Node("PrimaryDbUser")
        self.db_name = "postgres"

        status = self.com.get_db_cluster_status("detail")
        self.log.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

        text = "备份pg_hba.conf文件"
        self.log.info(text)
        self.hba = os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")
        result = self.common.get_sh_result(self.user_node,
                                           f"cp {self.hba} {self.hba}backup")
        self.assertNotIn("bash", result, "执行失败:" + text)
        self.assertNotIn("ERROR", result, "执行失败:" + text)
        self.html = os.path.join(macro.DB_INSTANCE_PATH, "query_0040.html")

        text = "备份postgresql.conf文件"
        self.log.info(text)
        self.file = os.path.join(macro.DB_INSTANCE_PATH,
                                 macro.DB_PG_CONFIG_NAME)
        result = self.common.get_sh_result(self.user_node,
                                           f"cp {self.file} "
                                           f"{self.file}backup")
        self.log.info(result)

    def test_guc_query(self):
        text = "--step1+2:修改参数并重启; expect:成功"
        self.log.info(text)
        param_list = ["enable_resource_track=on",
                      "enable_auto_clean_unique_sql=on",
                      "enable_wdr_snapshot=on",
                      "instr_unique_sql_count=100"]
        for param in param_list:
            res = self.com.execute_gsguc("set",
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         param)
            self.log.info(res)
            self.assertTrue(res)

        status = self.com.restart_db_cluster()
        self.log.info(status)
        sql = "show enable_resource_track;show enable_wdr_snapshot;" \
              "show enable_auto_clean_unique_sql;"
        self.log.info(sql)
        result = self.com.execut_db_sql(sql, dbname=self.db_name)
        self.assertIn("on", result, "执行失败:" + text)
        self.assertNotIn("off", result, "执行失败:" + text)

        text = "修改pg_hba文件;expect:设置成功"
        self.log.info(text)
        self.log.info("查询目标行号")
        info = "Unix domain socket connections"
        cmd = f"cat {self.hba}| grep -n '{info}'"
        self.log.info(cmd)
        result = self.common.get_sh_result(self.user_node, cmd)
        self.log.info(result)
        self.assertNotIn("bash", result, "执行失败:" + text)
        num = int(result.split(':')[0])
        num += 1
        self.log.info(num)
        self.log.info("添加主机trust信息")
        hba_info = f"host all all {self.user_node.ssh_host}/32 trust"
        self.log.info(hba_info)
        cmd = f"sed -i '{num}a {hba_info}' {self.hba}"
        self.log.info(cmd)
        result = self.common.get_sh_result(self.user_node, cmd)
        self.log.info(result)
        self.assertNotIn("bash", result, "执行失败:" + text)

        self.log.info("打印现存pg_hba文件信息")
        cmd = f"cat {self.hba}| tail -n +{num}"
        self.log.info(cmd)
        result = self.common.get_sh_result(self.user_node, cmd)
        self.log.info(result)
        self.assertIn(hba_info, result, "执行失败:" + text)

        self.log.info("重启使pg_hba修改生效")
        self.com.restart_db_cluster()
        is_started = self.com.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

        text = "--step3:生成快照s1; expect:成功"
        self.log.info(text)
        create_sql = "select create_wdr_snapshot()"
        result = self.com.execut_db_sql(create_sql, dbname=self.db_name)
        self.assertIn(self.constant.create_snapshot_success,
                      result, "执行失败:" + text)
        time.sleep(10)
        select_sql = "select snapshot_id from snapshot.snapshot " \
                     "order by start_ts desc limit 1;"
        result = self.com.execut_db_sql(select_sql, dbname=self.db_name)
        s1 = result.splitlines()[-2].strip()
        self.log.info(s1)

        text = "--step4:执行100+1 unique_sql，查看hash table记录条数; expect:成功"
        self.log.info(text)
        for j in range(45):
            tablename = f"unique_table_{j}"
            sql = f"drop table if exists {tablename};" \
                  f"create table {tablename}(a int, b int);" \
                  f"drop table if exists {tablename};"
            result = self.com.execut_db_sql(sql, dbname=self.db_name)
            self.assertNotIn("ERROR", result, "执行失败:" + text)
        sql = "select count(*) from dbe_perf.statement;"
        result = self.com.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(result)
        num = result.splitlines()[-2].strip()

        table_list = ["pg_extension", "pg_index", "pg_inherits",
                      "pg_class", "pg_proc", "pg_cast", "pg_object"]
        for i in range(100 - int(num)):
            sql = f"select count(*) from {table_list[i]}"
            res = self.com.execut_db_sql(sql, dbname=self.db_name)
            self.assertNotIn("ERROR", res)

        sql = "select count(*) from dbe_perf.statement;"
        result = self.com.execut_db_sql(sql, dbname=self.db_name)
        self.assertIn("100\n", result, "执行失败:" + text)

        self.log.info("触发自动淘汰")
        sql = "select count(va) from (select get_instr_unique_sql() as va);"
        result = self.com.execut_db_sql(sql, dbname=self.db_name)
        self.assertIn("91\n", result, "执行失败:" + text)

        self.log.info("修改记录数目为1000，以免再次触发自动淘汰")
        res = self.com.execute_gsguc("reload",
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f"instr_unique_sql_count=1000")
        self.assertTrue(res)

        text = "--step5:生成快照s2; expect:成功"
        self.log.info(text)
        result = self.com.execut_db_sql(create_sql, dbname=self.db_name)
        self.assertIn(self.constant.create_snapshot_success,
                      result, "执行失败:" + text)
        time.sleep(10)
        msg = self.com.execut_db_sql(select_sql, dbname=self.db_name)
        s2 = msg.splitlines()[-2].strip()
        self.log.info(s2)
        self.assertNotEqual(s1, s2, "执行失败:" + text)

        text = "--step6:生成快照s3; expect:成功"
        self.log.info(text)
        result = self.com.execut_db_sql(create_sql, dbname=self.db_name)
        self.assertIn(self.constant.create_snapshot_success,
                      result, "执行失败:" + text)
        time.sleep(10)
        result = self.com.execut_db_sql(select_sql, dbname=self.db_name)
        s3 = result.splitlines()[-2].strip()
        self.log.info(s3)
        self.assertNotEqual(s2, s3, "执行失败:" + text)


        text = "--step7:快照s1+s2 生成wdr报告; expect:生成失败"
        self.log.info(text)
        sql = f"\\a \\t \\o {self.html}"
        result = self.com.execut_db_sql(sql, dbname=self.db_name)
        self.assertIn("Output format is unaligned",
                      result, "执行失败:" + text)
        sql = f"select generate_wdr_report({s1}, {s2}, 'all', 'cluster');"
        result = self.com.execut_db_sql(sql, dbname=self.db_name)
        self.assertIn("ERROR:  Instance reset time is different",
                      result, "执行失败:" + text)

        text = "--step8:快照s1+s3 生成wdr报告; expect:生成失败"
        self.log.info(text)
        sql = f"select generate_wdr_report({s1}, {s3}, 'all', 'cluster');"
        result = self.com.execut_db_sql(sql, dbname=self.db_name)
        self.assertIn("ERROR:  Instance reset time is different",
                      result, "执行失败:" + text)

        text = "--step9:快照s2+s3 生成wdr报告; expect:生成成功"
        self.log.info(text)
        sql = f"select generate_wdr_report({s2}, {s3}, 'all', 'cluster');"
        result = self.com.execut_db_sql(sql, dbname=self.db_name)
        self.assertNotIn("ERROR:  Instance reset time is different",
                         result, "执行失败:" + text)

    def tearDown(self):
        text = "--step10:清理环境; expect:成功"
        self.log.info(text)
        self.log.info(f"恢复pg_hba.conf文件+删除{self.html}文件")
        cmd_result = self.common.get_sh_result(self.user_node,
                                           f"mv {self.hba}backup {self.hba};"
                                           f"rm -rf {self.html}")
        self.log.info(cmd_result)

        self.log.info("恢复postgresql.conf文件")
        mv_result = self.common.get_sh_result(self.user_node,
                                           f"mv {self.file}backup "
                                           f"{self.file}")
        self.log.info(mv_result)

        status = self.com.restart_db_cluster()
        self.log.info(status)
        status = self.com.get_db_cluster_status("detail")
        self.log.info(status)

        sql = "show enable_resource_track;show enable_wdr_snapshot;" \
              "show enable_auto_clean_unique_sql;show instr_unique_sql_count"
        self.log.info(sql)

        result = self.com.execut_db_sql(sql, dbname=self.db_name)

        self.assertIn("on", result, "执行失败:" + text)
        self.assertIn("off", result, "执行失败:" + text)
        self.assertIn("100\n", result, "执行失败:" + text)
        self.assertEqual("", cmd_result, "执行失败:" + text)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info("==Opengauss_Function_Guc_Query_Case0040 finish=")
