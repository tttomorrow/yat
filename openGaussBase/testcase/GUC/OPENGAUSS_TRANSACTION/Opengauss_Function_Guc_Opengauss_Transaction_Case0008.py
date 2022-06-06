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
Case Name   : 修改allow_concurrent_tuple_update为on，观察预期结果；
Description :
    1、查询allow_concurrent_tuple_update默认值；
    show allow_concurrent_tuple_update;
    2、修改allow_concurrent_tuple_update为on，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "allow_concurrent_tuple_update=abc"
    gs_om -t stop && gs_om -t start
    show allow_concurrent_tuple_update;
    3、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为on；
    3、恢复默认值成功；
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
                    "_Case0007开始执行==")
        self.constant = Constant()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc(self):
        LOGGER.info("查询allow_concurrent_tuple_update 期望：默认值on")
        sql_cmd = COMMONSH.execut_db_sql("show "
                                       "allow_concurrent_tuple_update;")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("方式三修改allow_concurrent_tuple_update为abc"
                    "期望：设置失败")
        result = COMMONSH.execut_db_sql("set allow_concurrent_tuple_update "
                                      "to 'abc';")
        self.assertIn("ERROR", result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show "
                                       "allow_concurrent_tuple_update;")
        if "on" != sql_cmd.split("\n")[-2].strip():
            raise Exception("allow_concurrent_tuple_update "
                            "is not default!")
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        LOGGER.info("==Opengauss_Function_Guc_Opengauss_Transaction"
                    "_Case0007执行结束==")
