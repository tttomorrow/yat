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
Case Name   : 修改参数password_policy,并校验生效
Description :
              1、查看password_policy默认值；
              show password_policy;
              2、创建用户，使用简单密码
              drop user if exists user227 cascade;
              create user user227 password '12345678';
              3、设置password_policy参数
              gs_guc set -N all -I all -c "password_policy=0"
              4、创建用户，使用简单密码
              drop user if exists user227 cascade;
              create user user227 password '12345678';
              5、恢复环境
              drop user if exists user227 cascade;
              gs_guc set -N all -I all -c "password_policy=1"
Expect      : 1、显示默认值；
              2、创建失败
              3、参数修改成功 重启成功
              4、创建成功
              5、恢复环境
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
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0227"
            " start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("步骤1：查看password_policy默认值，并校验；")
        sql_cmd = COMMONSH.execut_db_sql("show password_policy;")
        LOGGER.info(sql_cmd)
        self.assertEqual("1", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("步骤2：创建用户，使用简单密码")
        sql_cmd = COMMONSH.execut_db_sql(f"drop user "
            f"if exists user227 cascade;"
            f"create user user227 password '12345678';")
        LOGGER.info(sql_cmd)
        self.assertIn("ERROR", sql_cmd)
        self.assertNotIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)

        LOGGER.info("步骤3：设置password_policy参数")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"password_policy=0")
        self.assertTrue(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

        LOGGER.info("步骤4：创建用户，使用简单密码")
        sql_cmd = COMMONSH.execut_db_sql(f"drop user "
            f"if exists user227 cascade;"
            f"create user user227 password '12345678';")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertNotIn("ERROR", sql_cmd)

    def tearDown(self):
        LOGGER.info("步骤5：恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql(f"drop user "
            f"if exists user227 cascade")
        LOGGER.info(sql_cmd)
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"password_policy=1")
        LOGGER.info(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0227"
            " finish==")
