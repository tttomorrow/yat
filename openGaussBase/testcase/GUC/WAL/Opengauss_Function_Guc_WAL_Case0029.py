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
Case Name   : 修改参数enable_incremental_checkpoint为其他数据类型及超边界值，并校验其预期结果。
Description :
    1、查看enable_incremental_checkpoint默认值 期望：on；
    show enable_incremental_checkpoint;
    2、修改enable_incremental_checkpoint为'test'、12321等，期望：合理报错
    gs_guc reload -D {cluster/dn1} -c "enable_incremental_checkpoint=test";
    gs_guc reload -D {cluster/dn1} -c "enable_incremental_checkpoint=12321";
    3、恢复默认值 无需恢复
Expect      :
    1、查看enable_incremental_checkpoint默认值 期望：on；
    2、修改enable_incremental_checkpoint为'test'、12321等，期望：合理报错
    3、恢复默认值 无需恢复
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

logger = Logger()
commonsh = CommonSH("PrimaryDbUser")


class Guctestcase(unittest.TestCase):
    def setUp(self):
        logger.info("Opengauss_Function_Guc_WAL_Case0029开始执行")
        self.userNode = Node("PrimaryDbUser")
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()
        self.param = "enable_incremental_checkpoint"

    def test_guc_wal(self):
        text = f"--step1:查询{self.param};expect:环境值"
        logger.info(text)
        sql_cmd = commonsh.execut_db_sql(f"show {self.param};")
        logger.info(sql_cmd)
        self.assertIn("-----", sql_cmd, "执行失败" + text)
        self.value = sql_cmd.splitlines()[-2].strip()

        text = f"--step2:修改{self.param}为'test'、12321等;expect:合理报错,show参数为默认值"
        logger.info(text)
        value_list = ["'test'", 123321]
        for value in value_list:
            result = commonsh.execute_gsguc("reload",
                                            self.Constant.GSGUC_SUCCESS_MSG,
                                            f"{self.param}={value}")
            self.assertFalse(result)
            sql_cmd = commonsh.execut_db_sql(f"show {self.param};")
            logger.info(sql_cmd)
            self.assertIn(self.value, sql_cmd, "执行失败" + text)

    def tearDown(self):
        text = "--step3:恢复环境值;expect:成功"
        logger.info(text)
        commonsh.execute_gsguc("reload",
                               self.Constant.GSGUC_SUCCESS_MSG,
                               f"{self.param}={self.value}")
        commonsh.restart_db_cluster()
        is_started = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started,
                        "执行失败" + text)
        logger.info("Opengauss_Function_Guc_WAL_Case0029执行结束")
