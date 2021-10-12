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
Case Name   : 方式二修改参数enable_save_datachanged_timestamp为off
Description :
    步骤1:查询enable_save_datachanged_timestamp默认值
    show enable_save_datachanged_timestamp;
    步骤2:方式二修改enable_save_datachanged_timestamp为off，校验其预期结果
    gs_guc reload -N all -I all -c "enable_save_datachanged_timestamp=off"
    show enable_save_datachanged_timestamp;
    步骤3:执行DML
    步骤4:恢复默认值
Expect      :
    1、显示默认值on
    2、参数修改成功，校验修改后系统参数值为off
    3、改变表的数据，查询pg_stat_all_tables对应表的last_data_changed没有统计到时间戳
    4、恢复默认值成功；
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
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0067开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.param = "enable_save_datachanged_timestamp"

    def test_guc(self):
        LOGGER.info("步骤1 查询enable_save_datachanged_timestamp 期望：默认值on")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2 修改{self.param}为off，重启使其生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"{self.param}=off")
        self.assertTrue(result)

        LOGGER.info("期望：重启后查询结果为off")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤3 执行DML 期望：执行成功")
        sql_cmd = COMMONSH.execut_db_sql('''drop table if exists test cascade;
            create table test(c_int int);
            insert into test values(1),(2);
            update test set c_int = 5 where c_int = 1;
            delete from test where c_int = 2;
            select * from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)
        LOGGER.info("查询执行前后last_data_changed不变")
        result = COMMONSH.execut_db_sql("select last_data_changed "
            "from pg_stat_all_tables where relname='test';")
        LOGGER.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result)
        self.assertEqual("", result.splitlines()[-2].strip())

        LOGGER.info("步骤4 恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql("drop table test cascade;")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"{self.param}=on")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        if "on" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"{self.param}=on")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0067执行结束==")
