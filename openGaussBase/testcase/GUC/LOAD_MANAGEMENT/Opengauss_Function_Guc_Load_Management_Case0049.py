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
Case Name   : 修改session_history_memory为20*1024，观察预期结果；
Description :
    1、查询session_history_memory默认值 ；
    show session_history_memory;
    2、修改session_history_memory为20*1024，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "session_history_memory=20*1024"
    gs_om -t stop && gs_om -t start
    show session_history_memory;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值
    2、参数修改成功，校验修改后系统参数值为20MB
    3、DML无报错
    4、恢复默认值成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class GucTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info("Opengauss_Function_Guc_Load_Management_Case0049开始")
        self.Constant = Constant()
        self.commonsh = CommonSH("PrimaryDbUser")
        self.userNode = Node("PrimaryDbUser")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        text = "--step1:查询session_history_memory;expect:默认值10MB"
        self.logger.info(text)
        result = self.commonsh.execut_db_sql("show session_history_memory;")
        self.logger.info(result)
        self.assertEqual("10MB", result.split("\n")[-2].strip(),
                         "执行失败:" + text)

        text = "--step2:修改session_history_memory为20MB，重启使其生效;expect:设置成功"
        self.logger.info(text)
        result = self.commonsh.execute_gsguc("set",
                                             self.Constant.GSGUC_SUCCESS_MSG,
                                             "session_history_memory=20MB")
        self.assertTrue(result, "执行失败:" + text)

        self.logger.info("期望：重启后查询结果为设置值")
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        result = self.commonsh.execut_db_sql("show session_history_memory")
        self.logger.info(result)
        self.assertIn("20MB", result, "执行失败:" + text)

        text = "--step3:做DML;expect:无异常"
        self.logger.info(text)
        sql = '''drop table if exists test cascade;
                create table test(c_int int);
                insert into test values(1),(2);
                update test set c_int = 5 where c_int = 1;
                delete from test where c_int = 2;
                select * from test;
                drop table test cascade;'''
        result = self.commonsh.execut_db_sql(sql)
        self.logger.info(result)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], result,
                         "执行失败:" + text)

    def tearDown(self):
        text = "--step4:恢复默认值;expect:成功"
        self.logger.info(text)
        self.commonsh.execute_gsguc("set", self.Constant.GSGUC_SUCCESS_MSG,
                                    "session_history_memory=10MB")
        result = self.commonsh.restart_db_cluster()
        self.logger.info(result)

        status = self.commonsh.get_db_cluster_status()
        result = self.commonsh.execut_db_sql("show session_history_memory;")
        self.logger.info(result)

        self.assertEqual("10MB", result.split("\n")[-2].strip(),
                         "执行失败:" + text)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        "执行失败:" + text)
        self.logger.info("Opengauss_Function_Guc_Load_Management_Case0049结束")
