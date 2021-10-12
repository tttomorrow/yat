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
import time
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GucTestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0069开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.param = "enable_save_datachanged_timestamp"

    # 判断查询到的t为空 或为时间
    def is_timestamp(self, t):
        if t == "":
            return True
        LOGGER.info("last_data_changed:" + t)
        d_time = t.split('.')[0].strip()  # 2021-01-08 14:57:24.228786+08
        sql_cmd = COMMONSH.execut_db_sql(f"select date '{d_time}';")
        LOGGER.info(sql_cmd)
        return  "ERROR" not in sql_cmd

    def test_guc(self):
        LOGGER.info("步骤1:查询enable_save_datachanged_timestamp 期望：默认值on")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:方式四修改参数enable_save_datachanged_timestamp为off")
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
            self.assertTrue(self.is_timestamp(data1))

            time.sleep(3)
            LOGGER.info("步骤3:创建表做DML")
            sql_cmd = COMMONSH.execut_db_sql(f'''{sql}''')
            LOGGER.info(sql_cmd)
            self.assertNotIn("ERROR", sql_cmd)

            LOGGER.info("查询执行后last_data_changed")
            sql_cmd = COMMONSH.execut_db_sql("select last_data_changed "
                "from PG_STAT_ALL_TABLES where relname='test';")
            LOGGER.info(sql_cmd)
            self.assertNotIn("ERROR", sql_cmd)
            data2 = sql_cmd.splitlines()[-2].strip()
            self.assertTrue(self.is_timestamp(data2))
            LOGGER.info("判断前后时间不同 操作时间已更新")
            self.assertNotEqual(data1, data2)

        LOGGER.info("步骤3:恢复默认值")
        LOGGER.info("步骤3:恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("drop table test cascade;"
            "drop table test1 cascade;")
        LOGGER.info(sql_cmd)
        self.assertNotIn("ERROR", sql_cmd)
        data1 = sql_cmd.splitlines()[-2].strip()
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"{self.param}='on'")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        if "on" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"{self.param}='on'")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0069执行结束==")
