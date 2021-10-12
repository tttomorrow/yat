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
Case Name   : 修改xc_maintenance_mode为on，观察预期结果；
Description :
    1、查询xc_maintenance_mode默认值；
    show xc_maintenance_mode;
    2、修改xc_maintenance_mode为on，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "xc_maintenance_mode=abc"
    gs_om -t stop && gs_om -t start
    show xc_maintenance_mode;
    3、执行ddl验证是否read_only
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为off；
    3、ddl报错ERROR in a read-only transaction
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
                    "_Case0006开始执行==")
        self.constant = Constant()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc(self):
        LOGGER.info("查询xc_maintenance_mode 期望：默认值off")
        sql_cmd = COMMONSH.execut_db_sql("show xc_maintenance_mode;")
        LOGGER.info(sql_cmd)
        self.assertIn("off", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("方式三修改xc_maintenance_mode为abc，期望：设置失败")
        result = COMMONSH.execut_db_sql("set xc_maintenance_mode to 'abc';")
        self.assertIn("ERROR", result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show xc_maintenance_mode;")
        if "off" != sql_cmd.split("\n")[-2].strip():
            raise Exception("xc_maintenance_mode is not default!")
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        LOGGER.info("==Opengauss_Function_Guc_Opengauss_Transaction"
                    "_Case0006执行结束==")
