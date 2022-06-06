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
Case Name   : 方式四修改参数enable_save_datachanged_timestamp为off
Description :
    步骤1:查询enable_save_datachanged_timestamp默认值
    show enable_save_datachanged_timestamp;
    步骤2:方式四修改参数enable_save_datachanged_timestamp为off
    alter system set enable_save_datachanged_timestamp to off;
    show enable_save_datachanged_timestamp;
    步骤3:恢复默认值
    alter system set enable_save_datachanged_timestamp to on;
Expect      :
    步骤1:显示默认值on
    步骤2:参数设置失败合理报错，校验参数值为on
    步骤3:恢复默认值成功
History     :
"""
import os
import time
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GucTestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0069开始执行==")
        self.constant = Constant()
        self.common = Common()
        self.com = CommonSH("PrimaryDbUser")
        self.user_node = Node("PrimaryDbUser")
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.param = "enable_save_datachanged_timestamp"

        text = "备份pg_hba.conf文件"
        LOGGER.info(text)
        self.hba = os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")
        result = self.common.get_sh_result(self.user_node,
                                           f"cp {self.hba} {self.hba}backup")
        self.assertNotIn("bash", result, "执行失败:" + text)
        self.assertNotIn("ERROR", result, "执行失败:" + text)
        
    def test_guc(self):
        LOGGER.info(f"--修改参数 确认落盘--")
        result = COMMONSH.execute_gsguc("set",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"synchronous_standby_names='*'")
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc("set",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"synchronous_commit='remote_apply'")
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc("set",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"hot_standby=on")
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc("set",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"wal_level='hot_standby'")
        self.assertTrue(result)
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status()
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

        LOGGER.info(f"--step1:查询{self.param};expect:默认值on")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertEqual("on", sql_cmd.splitlines()[-2].strip())

        LOGGER.info(f"--step2:方式四修改参数{self.param}为off;expect:失败")
        sql_cmd = COMMONSH.execut_db_sql(f"alter system "
            f"set {self.param} to off;show {self.param};")
        self.assertIn("ERROR", sql_cmd)
        self.assertIn("on\n", sql_cmd)

        LOGGER.info("创建表,执行insert/update/delete, "
                    "exchange/truncate/drop partition，查看last_data_changed被统计")
        sql_cmd = COMMONSH.execut_db_sql('''drop table if exists test;\
            create table test(c_int int) PARTITION BY RANGE(c_int)\
            (PARTITION P1 VALUES LESS THAN(100),\
            PARTITION P2 VALUES LESS THAN(200),\
            PARTITION P3 VALUES LESS THAN(300));\
            insert into test values(11),(12),(285),(286);\
            drop table if exists test1;create table test1(c_int int);\
            insert into test1 values(201),(205),(208);
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn("ERROR", sql_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd)

        sql_list = ["alter table test truncate PARTITION p1;",
                    "insert into test values(1),(2),(255),(256);",
                    "update test set c_int = 5 where c_int = 1;",
                    "delete from test where c_int = 2;",
                    "alter table test EXCHANGE PARTITION (P3) "
                    "WITH TABLE test1;",
                    "alter table test DROP PARTITION P2;"]
        for sql in sql_list:
            LOGGER.info("查询执行前last_data_changed")
            sql_cmd = COMMONSH.execut_db_sql("select last_data_changed "
                "from PG_STAT_ALL_TABLES where relname='test';")
            LOGGER.info(sql_cmd)
            self.assertNotIn("ERROR", sql_cmd)
            data1 = sql_cmd.splitlines()[-2].strip()

            time.sleep(3)
            LOGGER.info("--校验功能")
            sql_cmd = COMMONSH.execut_db_sql(f'''{sql}''')
            LOGGER.info(sql_cmd)
            self.assertNotIn("ERROR", sql_cmd)

            LOGGER.info("查询执行后last_data_changed")
            sql_cmd = COMMONSH.execut_db_sql("select last_data_changed "
                "from PG_STAT_ALL_TABLES where relname='test';")
            LOGGER.info(sql_cmd)
            self.assertNotIn("ERROR", sql_cmd)
            data2 = sql_cmd.splitlines()[-2].strip()
            LOGGER.info("判断前后时间不同 操作时间已更新")
            self.assertNotEqual(data1, data2)

    def tearDown(self):
        LOGGER.info("--step3:恢复默认值;expect:成功")
        LOGGER.info(f"恢复pg_hba.conf文件")
        cmd_result = self.common.get_sh_result(self.user_node,
                                           f"mv {self.hba}backup {self.hba}")
        LOGGER.info(cmd_result)

        sql_result = COMMONSH.execut_db_sql("drop table test cascade;"
                                            "drop table test1 cascade;")
        LOGGER.info(sql_result)
        COMMONSH.execute_gsguc("reload",
                              self.constant.GSGUC_SUCCESS_MSG,
                              f"{self.param}='on'")
        COMMONSH.restart_db_cluster()
        result = COMMONSH.execut_db_sql(f"show {self.param};")
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("on\n" in result)
        self.assertNotIn("ERROR", sql_result)
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0069执行结束==")
