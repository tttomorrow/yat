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
Case Name   : 修改enable_resource_record为on，观察预期结果；
Description :
    1、查询enable_resource_record默认值 ；
    show enable_resource_record;
    2、修改enable_resource_record为on，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "enable_resource_track=on"
    gs_guc set -D {cluster/dn1} -c "resource_track_level=operator"
    gs_guc set -D {cluster/dn1} -c "enable_resource_record=on"
    gs_guc set -D {cluster/dn1} -c "resource_track_duration=0"
    gs_guc set -D {cluster/dn1} -c "resource_track_cost=9"
    gs_guc set -D {cluster/dn1} -c "use_workload_manager=on"
    gs_om -t stop && gs_om -t start
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值
    2、参数修改成功，校验修改后系统参数值为on
    3、DML无报错 查询gs_wlm_plan_operator_history有新增数据
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
        self.logger.info("Opengauss_Function_Guc_Load_Management_Case0013开始")
        self.Constant = Constant()
        self.commonsh = CommonSH("PrimaryDbUser")
        self.userNode = Node("PrimaryDbUser")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        text = "--step1:查询enable_resource_record;expect:默认值off"
        self.logger.info(text)
        result = self.commonsh.execut_db_sql("show enable_resource_record;")
        self.logger.info(result)
        self.assertEqual("off", result.split("\n")[-2].strip(),
                         "执行失败:" + text)

        text = "--step2:修改enable_resource_record为on，重启使其生效;expect:设置成功"
        self.logger.info(text)
        result = self.commonsh.execute_gsguc("set",
                                             self.Constant.GSGUC_SUCCESS_MSG,
                                             "enable_resource_track=on")
        self.assertTrue(result, "执行失败:" + text)
        result = self.commonsh.execute_gsguc("set",
                                             self.Constant.GSGUC_SUCCESS_MSG,
                                             "resource_track_level=operator")
        self.assertTrue(result, "执行失败:" + text)
        result = self.commonsh.execute_gsguc("set",
                                             self.Constant.GSGUC_SUCCESS_MSG,
                                             "resource_track_duration=0")
        self.assertTrue(result, "执行失败:" + text)
        result = self.commonsh.execute_gsguc("set",
                                             self.Constant.GSGUC_SUCCESS_MSG,
                                             "enable_resource_record=on")
        self.assertTrue(result, "执行失败:" + text)
        result = self.commonsh.execute_gsguc("set",
                                             self.Constant.GSGUC_SUCCESS_MSG,
                                             "resource_track_cost=9")
        self.assertTrue(result, "执行失败:" + text)
        result = self.commonsh.execute_gsguc("set",
                                             self.Constant.GSGUC_SUCCESS_MSG,
                                             "use_workload_manager=on")
        self.assertTrue(result, "执行失败:" + text)

        text = "期望：重启后查询结果为设置值"
        self.logger.info(text)
        status = self.commonsh.restart_db_cluster()
        self.logger.info(status)
        sql = "show enable_resource_track;show resource_track_level;" \
              "show enable_resource_record;show resource_track_cost;" \
              "show use_workload_manager;show resource_track_duration;"
        result = self.commonsh.execut_db_sql(sql)
        self.logger.info(result)
        self.assertIn("on", result, "执行失败:" + text)
        self.assertNotIn("off", result, "执行失败:" + text)
        self.assertIn("operator", result, "执行失败:" + text)
        self.assertIn("9", result, "执行失败:" + text)
        self.assertIn("0", result, "执行失败:" + text)

        self.logger.info("查询gs_wlm_plan_operator_history数据量")
        result_bef = self.commonsh.execut_db_sql(f"select count(*) "
            f"from gs_wlm_plan_operator_history "
            f"where datname='{self.userNode.db_name}'")
        self.logger.info(result_bef)

        text = "--step3:做DML;expect:无异常"
        self.logger.info(text)
        sql = '''begin
                for i in  0..1000 loop
                    drop table if exists test cascade;
                    create table test(c_int int);
                    insert into test values(1),(2);
                    update test set c_int = 5 where c_int = 1;
                    delete from test where c_int = 2;
                end loop;
                end;
                select * from test;
                drop table test;'''
        result = self.commonsh.execut_db_sql(sql)
        self.logger.info(result)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], result,
                         "执行失败:" + text)

        self.logger.info("查询gs_wlm_plan_operator_history数据量增长")
        result_aft = self.commonsh.execut_db_sql(
             f"select count(*) from gs_wlm_plan_operator_history "
             f"where datname='{self.userNode.db_name}'")
        self.logger.info(result_aft)
        self.assertGreater(int(result_aft.split("\n")[-2].strip()),
                                int(result_bef.split("\n")[-2].strip()),
                                "执行失败:" + text)

    def tearDown(self):
        text = "--step4:恢复默认值;expect:成功"
        self.logger.info(text)
        result_list = []
        param_list = ["enable_resource_track=on",
                      "resource_track_level=query",
                      "resource_track_duration=60",
                      "enable_resource_record=off",
                      "resource_track_cost=100000",
                      "use_workload_manager=off"]
        for param in param_list:
            result = self.commonsh.execute_gsguc("set",
                                                 self.Constant.
                                                 GSGUC_SUCCESS_MSG,
                                                 param)
            result_list.append(result)

        self.commonsh.restart_db_cluster()

        sql = "show enable_resource_track;show resource_track_level;" \
              "show enable_resource_record;show resource_track_cost;" \
              "show use_workload_manager;show resource_track_duration;"
        sql_result = self.commonsh.execut_db_sql(sql)
        self.logger.info(sql_result)

        status = self.commonsh.get_db_cluster_status()

        for result in result_list:
            self.assertTrue(result, "执行失败:" + text)

        self.assertIn("on", sql_result, "执行失败:" + text)
        self.assertIn("off", sql_result, "执行失败:" + text)
        self.assertIn("query", sql_result, "执行失败:" + text)
        self.assertIn("100000", sql_result, "执行失败:" + text)
        self.assertIn("1min", sql_result, "执行失败:" + text)

        self.assertTrue("Degraded" in status or "Normal" in status,
                        "执行失败:" + text)
        self.logger.info("Opengauss_Function_Guc_Load_Management_Case0013结束")
