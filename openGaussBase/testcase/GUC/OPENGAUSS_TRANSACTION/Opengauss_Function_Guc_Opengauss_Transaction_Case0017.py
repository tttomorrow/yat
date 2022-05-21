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
Case Name   : 修改replication_type为0，观察预期结果；
Description :
    1、查询replication_type默认值；
    show replication_type;
    2、修改replication_type为0，restart集群，校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "replication_type=0"
    gs_om -t restart
    3、恢复默认值
Expect      :
    1、显示默认值；
    2、参数修改成功，restart失败
    3、恢复默认值成功
History     :
"""

import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 == COMMONSH.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class Guctestcase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("==Opengauss_Function_Guc_Opengauss_Transaction"
                      "_Case0017开始执行==")
        self.constant = Constant()
        self.com = Common()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc(self):
        text = "--step1:查询replication_type ;expect:默认值1"
        self.log.info(text)
        sql_cmd = COMMONSH.execut_db_sql("show replication_type;")
        self.log.info(sql_cmd)
        self.assertIn("1\n", sql_cmd, "执行失败" + text)

        text = "--step2:方式一修改replication_type为0,restart集群;expect:restart失败"
        self.log.info(text)
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "replication_type=0")
        self.assertTrue(result, "执行失败" + text)

        result = COMMONSH.restart_db_cluster()
        self.assertFalse(result, "执行失败" + text)

    def tearDown(self):
        text = "--step3:恢复默认值;expect:成功"
        self.log.info(text)
        COMMONSH.execute_gsguc("set",
                               self.constant.GSGUC_SUCCESS_MSG,
                               "replication_type=1")
        result = COMMONSH.restart_db_cluster()
        self.log.info(result)

        result = self.com.show_param("replication_type")
        self.log.info(result)
        is_started = COMMONSH.get_db_cluster_status()

        self.assertEqual("1", result, "执行失败" + text)
        self.assertTrue("Degraded" in is_started or "Normal" in is_started,
                        "执行失败" + text)
        self.log.info("==Opengauss_Function_Guc_Opengauss_Transaction"
                      "_Case0017执行结束==")
