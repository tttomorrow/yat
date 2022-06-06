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
Case Name   : 修改enable_show_any_tuples为on，观察预期结果；
Description :
    1、查询enable_show_any_tuples默认值；
    show enable_show_any_tuples;
    2、修改enable_show_any_tuples为on，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "enable_show_any_tuples=on"
    gs_om -t stop && gs_om -t start
    show enable_show_any_tuples;
    3、执行ddl
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为off；
    3、ddl无报错
    4、恢复默认值成功；
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
        LOGGER.info("==Opengauss_Function_Guc_Opengauss_Transaction"
            "_Case0015开始执行==")
        self.constant = Constant()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc(self):
        LOGGER.info("查询enable_show_any_tuples 期望：默认值off")
        sql_cmd = COMMONSH.execut_db_sql("show enable_show_any_tuples;")
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("方式一修改enable_show_any_tuples为on"
                    "重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "enable_show_any_tuples=on")
        self.assertTrue(result)

        LOGGER.info("期望：重启后查询结果为on")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql("show enable_show_any_tuples;")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.split("\n")[-2].strip())

        sql_cmd = COMMONSH.execut_db_sql('''drop table if exists test;
            create table test(c_int int);insert into test values(1);
            update test set c_int = 2;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn("ERROR", sql_cmd)

        sql_cmd = COMMONSH.execut_db_sql('''START TRANSACTION ISOLATION \
            LEVEL READ COMMITTED READ ONLY;\
                SELECT * FROM test;\
            COMMIT;\
            ''')
        LOGGER.info(sql_cmd)
        self.assertIn("1\n", sql_cmd)
        self.assertIn("2\n", sql_cmd)

        LOGGER.info("恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql("drop table test cascade;")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"enable_show_any_tuples=off")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show enable_show_any_tuples;")
        if "off" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                   "enable_show_any_tuples=off")
            COMMONSH.restart_db_cluster()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        LOGGER.info("==Opengauss_Function_Guc_Opengauss_Transaction"
            "_Case0015执行结束==")
