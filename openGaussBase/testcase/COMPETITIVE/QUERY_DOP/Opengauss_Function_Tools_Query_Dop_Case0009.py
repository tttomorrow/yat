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
Case Type   : Query_Dop并行查询
Case Name   : 将并行查询参数设置为包含单引号的字符'1'
Description :
    1、更改query_dop参数的值为包含单引号的字符'1'
    2、重新启动数据库集群
    3、查看query_dop参数是否生效
    4、清理环境
Expect      :
    1、更改query_dop参数成功
    2、重新启动数据库集群成功
    3、查看参数已生效
    4、清理环境
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class QueryDopCase(unittest.TestCase):

    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            "---Opengauss_Function_Tools_Query_Dop_Case0009开始执行---")
        self.constant = Constant()
        self.commonsh = CommonSH("PrimaryDbUser")
        self.common = Common()
        self.initial_query_dop = self.common.show_param("query_dop")

    def test_query_dop(self):
        step1_text = "---step1:更改query_dop参数的值为包含单引号的字符'1';expect:更改参数成功---"
        self.logger.info(step1_text)
        guc_cmd = self.commonsh.execute_gsguc("set",
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              "query_dop = '1'")
        self.logger.info(guc_cmd)
        self.assertTrue(guc_cmd, "执行失败:" + step1_text)

        step2_text = "---step2:重新启动数据库集群;expect:重启数据库成功---"
        self.logger.info(step2_text)
        gs_cmd = self.commonsh.restart_db_cluster()
        self.logger.info(gs_cmd)
        self.logger.info("---检查数据库状态是否正常---")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

        step3_text = "---step3:查看参数;expect:修改成功---"
        self.logger.info(step3_text)
        sql_cmd = self.commonsh.execut_db_sql("show query_dop")
        self.logger.info(sql_cmd)
        self.common.equal_sql_mdg(sql_cmd, "query_dop", "1",
                                  "(1 row)", flag="1")

    def tearDown(self):
        self.logger.info("---清理环境,改回参数初始值并重启数据库集群---")
        qu_cmd = self.commonsh.execute_gsguc("set",
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f"query_dop = "
                                             f"{self.initial_query_dop}")
        self.logger.info(qu_cmd)
        restart_text = "---重启数据库集群---"
        self.logger.info(restart_text)
        restart_cmd = self.commonsh.restart_db_cluster()
        self.logger.info(restart_cmd)
        self.logger.info("---检查数据库状态是否正常---")
        status_res = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status_res or "Normal" in status_res)
        self.logger.info(
            "---Opengauss_Function_Tools_Query_Dop_Case0009执行结束---")
