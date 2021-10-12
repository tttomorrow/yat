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
Case Name   : 修改参数modify_initial_password,并校验不生效
Description :
              1、查看modify_initial_password默认值；
              show modify_initial_password;
              2、设置modify_initial_password参数
              gs_guc set -N all -I all -c "modify_initial_password=on"
              3、初始用户连接，执行select
              select 1;
              4、恢复环境
              drop user if exists user220 cascade;
              gs_guc set -N all -I all -c "modify_initial_password=off"
Expect      : 1、显示默认值；
              2、参数修改成功 重启成功
              3、select成功
              4、恢复环境
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class Guctestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0220"
            " start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.user_node = Node("PrimaryDbUser")

    def test_guc(self):
        LOGGER.info("步骤1：查看modify_initial_password默认值，并校验；")
        sql_cmd = COMMONSH.execut_db_sql("show modify_initial_password;")
        LOGGER.info(sql_cmd)
        self.assertEqual("off", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("步骤2：设置modify_initial_password参数")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"modify_initial_password=on")
        self.assertTrue(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

        LOGGER.info("步骤3：初始用户连接，执行select")
        excute_cmd = f'''source {macro.DB_ENV_PATH};\
            gsql \
            -d {self.user_node.db_name} \
            -p {self.user_node.db_port} \
            -c "select 1;"
            '''
        LOGGER.info(excute_cmd)
        result = self.user_node.sh(excute_cmd).result()
        LOGGER.info(result)
        self.assertNotIn("ERROR", result)
        self.assertIn("1", result)

    def tearDown(self):
        LOGGER.info("步骤4：恢复默认值")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"modify_initial_password=off")
        LOGGER.info(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0220"
            " finish==")
