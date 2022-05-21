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
Case Name   : 修改参数password_reuse_max,并校验生效
Description : 1、查看password_reuse_max默认值；
              source {env}
              show password_reuse_max;
              show password_reuse_max;
              2、设置password_reuse_max参数
              gs_guc set -N all -I all -c "password_reuse_max=1"
              3、创建用户，修改为旧密码
              drop user if exists user2 cascade;
              create user user2 password '{macro.COMMON_PASSWD}';
              alter role user2 identified by '{self.temp_paasswd}'
              replace '{macro.COMMON_PASSWD}';
              alter role user2 identified by '{macro.COMMON_PASSWD}'
              replace '{self.temp_paasswd1}';
              alter role user2 identified by '{self.temp_paasswd1}'
              replace '{self.temp_paasswd2}';
              alter role user2 identified by '{self.temp_paasswd2}'
              replace '{macro.COMMON_PASSWD}';
              4、恢复环境
              drop user if exists user2 cascade;
              gs_guc set -N all -I all -c "password_reuse_max=60"
Expect      : 1、显示默认值；
              2、参数修改成功 重启成功
              3、修改为旧密码成功
              4、恢复环境
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class Guctestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0267"
            " start==")
        self.constant = Constant()
        self.temp_paasswd1 = macro.COMMON_PASSWD + "test"
        self.temp_paasswd2 = macro.COMMON_PASSWD + "test1"

    def test_guc(self):
        LOGGER.info("步骤1：查看password_reuse_max默认值，并校验；")
        sql_cmd = COMMONSH.execut_db_sql("show password_reuse_max;")
        LOGGER.info(sql_cmd)
        self.assertEqual("0", sql_cmd.split("\n")[-2].strip())
        sql_cmd = COMMONSH.execut_db_sql("show password_reuse_time;")
        LOGGER.info(sql_cmd)
        self.assertEqual("60", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("步骤2：设置password_reuse_max参数")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"password_reuse_time=0")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"password_reuse_max=1")
        self.assertTrue(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

        LOGGER.info("步骤3：创建用户，修改为旧密码成功")
        sql_cmd = COMMONSH.execut_db_sql(f"drop user if exists user2 cascade;"
            f"create user user2 password '{macro.COMMON_PASSWD}';"
            f"alter role user2 identified by "
            f"'{self.temp_paasswd1}' replace '{macro.COMMON_PASSWD}';"
            f"alter role user2 identified by "
            f"'{self.temp_paasswd2}' replace '{self.temp_paasswd1}';"
            f"alter role user2 identified by "
            f"'{macro.COMMON_PASSWD}' replace '{self.temp_paasswd2}';")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertNotIn("ERROR", sql_cmd)

        LOGGER.info("步骤4：恢复环境")
        sql_cmd = COMMONSH.execut_db_sql(f"drop user if exists user2 cascade")
        LOGGER.info(sql_cmd)
        self.assertNotIn("ERROR", sql_cmd)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, sql_cmd)

        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"password_reuse_time=60")
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"password_reuse_max=0")
        self.assertTrue(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql(f"drop user if exists user2 cascade")
        LOGGER.info(sql_cmd)
        sql_cmd1 = COMMONSH.execut_db_sql("show password_reuse_time;")
        sql_cmd2 = COMMONSH.execut_db_sql("show password_reuse_max;")
        if "60" != sql_cmd1.split("\n")[-2].strip() or "0" != \
                sql_cmd2.split("\n")[-2].strip():
            result = COMMONSH.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"password_reuse_max=60")
            LOGGER.info(result)
            result = COMMONSH.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"password_reuse_max=0")
            LOGGER.info(result)
            COMMONSH.restart_db_cluster()
            status = COMMONSH.get_db_cluster_status()
            self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0267"
            " finish==")
