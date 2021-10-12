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
Case Name   : 修改cn_send_buffer_size为其他数据类型，观察其预期结果；
Description :
            1、查询cn_send_buffer_size默认值；
            show cn_send_buffer_size；
            2、修改cn_send_buffer_size为16，观察预期结果；
            gs_guc set -D {cluster/dn1}  -c "cn_send_buffer_size=16"
            3、恢复默认值
Expect      :
            1、显示默认值8kB；
            2、修改cn_send_buffer_size成功，预期结果正常；
            3、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GucTest(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Error_Tolerance_Case0008"
                    "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("==查询cn_send_buffer_size 期望：默认值8kB==")
        sql_cmd = COMMONSH.execut_db_sql("show cn_send_buffer_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("8kB", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("修改cn_send_buffer_size为16重启生效，期望设置成功")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "cn_send_buffer_size=16")
        self.assertTrue(result)

        LOGGER.info("期望：重启后查询结果为16kB")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql("show cn_send_buffer_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("16kB", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("做DML")
        sql_cmd = COMMONSH.execut_db_sql('''
            drop table if exists test cascade;
            create table test(c_int int);
            begin
                for i in 0..100 loop
                    insert into test values(i);
                    update test set c_int = 66 where c_int = i;
                end loop;
            end;
            select count(*) from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        LOGGER.info("恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql(
            "drop table if exists test cascade;")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "cn_send_buffer_size=8")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show cn_send_buffer_size;")
        LOGGER.info(sql_cmd)
        if "8kB" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  "cn_send_buffer_size=8")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        sql_cmd = COMMONSH.execut_db_sql("show cn_send_buffer_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("8kB", sql_cmd.split("\n")[-2].strip())
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Error_Tolerance_Case0008"
                    "执行结束==")
