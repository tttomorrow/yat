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
Case Name   : 方式二修改参数track_thread_wait_status_interval为60,设置成功并生效
Description :
    步骤1:查询track_thread_wait_status_interval默认值
    show track_thread_wait_status_interval;
    步骤2:方式二修改track_thread_wait_status_interval为no，校验其预期结果
    gs_guc reload -N all -I all -c "track_thread_wait_status_interval=60"
    show track_thread_wait_status_interval;
    步骤3:做简单DML
    步骤4:恢复默认值
Expect      :
    步骤1:显示默认值30min
    步骤2:参数修改成功，校验修改后参数值为1h
    步骤3:DML无报错
    步骤4:恢复默认值成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GucTestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0061"
            "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_guc(self):
        LOGGER.info("查询track_thread_wait_status_interval 期望：默认值30min")
        sql_cmd = COMMONSH.execut_db_sql(
            "show track_thread_wait_status_interval;")
        LOGGER.info(sql_cmd)
        self.assertEqual("30min", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("修改track_thread_wait_status_interval为on，重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_thread_wait_status_interval=60")
        self.assertTrue(result)

        LOGGER.info("期望：重启后查询结果为on")
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status()
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        sql_cmd = COMMONSH.execut_db_sql("show "
            "track_thread_wait_status_interval;")
        LOGGER.info(sql_cmd)
        self.assertEqual("1h", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("执行DML 期望：执行成功")
        sql_cmd = COMMONSH.execut_db_sql('''
            begin
                for i in  0..10 loop
                    drop table if exists test cascade;
                    create table test(c_int int);
                    insert into test values(1),(2);
                    update test set c_int = 5 where c_int = 1;
                    delete from test where c_int = 2;
                end loop;
            end;
            select * from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        LOGGER.info("恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql("drop table test cascade;")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_thread_wait_status_interval="
                                       "30min")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql(
            "show track_thread_wait_status_interval;")
        if "30min" not in sql_cmd:
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  'track_thread_wait_status_interval=30min')
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0061"
            "执行结束==")
