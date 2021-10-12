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
Case Name   : 方式二修改参数track_io_timing为yes/true/1,设置成功并生效
Description :
    1、查询track_io_timing默认值
    show track_io_timing;
    2、方式二修改track_io_timing为yes，校验其预期结果
    gs_guc reload -N all -I all -c "track_io_timing=yes"
    show track_io_timing;
    3、方式二修改track_io_timing为true，校验其预期结果
    gs_guc reload -N all -I all -c "track_io_timing=true"
    show track_io_timing;
    4、方式二修改track_io_timing为1，校验其预期结果
    gs_guc reload -N all -I all -c "track_io_timing=1"
    show track_io_timing;
    5、做简单DML
    6、恢复默认值
Expect      :
    1、显示默认值off
    2、参数修改成功，校验修改后参数值为on
    3、参数修改成功，校验修改后参数值为on
    4、参数修改成功，校验修改后参数值为on
    5、DML无报错
    6、恢复默认值成功
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
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0039"
                    "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("1、查询track_io_timing 期望：默认值off")
        sql_cmd = COMMONSH.execut_db_sql("show track_io_timing;")
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("2、修改track_io_timing为yes，重启生效 期望设置成功")
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_io_timing=yes")
        self.assertTrue(result)
        LOGGER.info("期望：查询结果为on")
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)
        sql_cmd = COMMONSH.execut_db_sql("show track_io_timing;")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("3、修改track_io_timing为true，重启生效 期望设置成功")
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_io_timing=true")
        self.assertTrue(result)
        LOGGER.info("期望：查询结果为on")
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)
        sql_cmd = COMMONSH.execut_db_sql("show track_io_timing;")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("4、修改track_io_timing为1，重启生效，期望：设置成功")
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_io_timing=1")
        self.assertTrue(result)
        LOGGER.info("期望：查询结果为on")
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)
        sql_cmd = COMMONSH.execut_db_sql("show track_io_timing;")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("5、做DML不报错")
        sql_cmd = COMMONSH.execut_db_sql('''drop table if exists test;
            create table test(c_int int);
            insert into test values(1),(2);
            update test set c_int = 5 where c_int = 1;
            delete from test where c_int = 2;
            select * from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        LOGGER.info("6、恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql("drop table test cascade;")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_io_timing=off")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show track_io_timing;")
        if "off" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  "track_io_timing=off")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0039"
                    "执行结束==")
