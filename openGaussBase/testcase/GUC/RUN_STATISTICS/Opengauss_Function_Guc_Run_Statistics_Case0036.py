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
Case Name   : 管理员用户方式三修改参数track_counts为0/true/no,设置成功并生效
Description :
    1、查询track_counts默认值
    show track_counts;
    2、管理员用户方式三修改track_counts为0
    alter database postgres set track_counts to 0;
    show track_counts;
    管理员用户方式三修改track_counts为true
    alter database postgres set track_counts to true;
    show track_counts;
    管理员用户方式三修改track_counts为no
    alter database postgres set track_counts to no;
    show track_counts;
    3、恢复默认值,清理环境
Expect      :
    1、显示默认值
    2、参数设置成功
    3、恢复默认值成功
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


class GucTestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0036"
                    "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.user_node = Node("PrimaryDbUser")
        self.db_name = 'testdb'

    def test_guc(self):
        LOGGER.info("1、查询track_counts 期望：默认值on")
        sql_cmd = COMMONSH.execut_db_sql("show track_counts;")
        LOGGER.info(sql_cmd)
        self.assertEqual("on", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("2、管理员用户方式三修改参数track_counts为0")
        sql_cmd = COMMONSH.execut_db_sql(f"drop database if exists;"
            f"create database  {self.db_name};"
            f"alter database  {self.db_name} set track_counts to 0;")
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)

        sql_cmd = ("show track_counts;")
        excute_cmd = f'''source {macro.DB_ENV_PATH};\
            gsql -d  {self.db_name} -U {self.user_node.db_user}\
            -p {self.user_node.db_port} \
            -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
            '''
        LOGGER.info(excute_cmd)
        result = self.user_node.sh(excute_cmd).result()
        LOGGER.info(result)
        self.assertIn("off\n", result)

        LOGGER.info("管理员用户方式三修改参数track_counts为true")
        sql_cmd = COMMONSH.execut_db_sql(f"alter database "
            f" {self.db_name} set track_counts to true;")
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)

        sql_cmd = ("show track_counts;")
        excute_cmd = f'''source {macro.DB_ENV_PATH};\
            gsql -d  {self.db_name} -U {self.user_node.db_user}\
            -p {self.user_node.db_port} \
            -W {macro.COMMON_PASSWD} -c "{sql_cmd}"'''
        LOGGER.info(excute_cmd)
        result = self.user_node.sh(excute_cmd).result()
        LOGGER.info(result)
        self.assertIn("on\n", result)

        LOGGER.info("管理员用户方式三修改参数track_counts为no")
        sql_cmd = COMMONSH.execut_db_sql(f"alter database "
            f" {self.db_name} set track_counts to no;")
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)

        sql_cmd = ("show track_counts;")
        excute_cmd = f'''source {macro.DB_ENV_PATH};\
            gsql -d  {self.db_name} -U {self.user_node.db_user}\
            -p {self.user_node.db_port} \
            -W {macro.COMMON_PASSWD} -c "{sql_cmd}"'''
        LOGGER.info(excute_cmd)
        result = self.user_node.sh(excute_cmd).result()
        LOGGER.info(result)
        self.assertIn("off\n", result)

        LOGGER.info("3、恢复默认值")
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_counts=on")
        self.assertTrue(result)
        sql_cmd = COMMONSH.execut_db_sql(f"drop database  {self.db_name};")
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, sql_cmd)

        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        COMMONSH.execut_db_sql(f"drop database if exists  {self.db_name};")
        sql_cmd = COMMONSH.execut_db_sql("show track_counts;")
        if "on" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  "track_counts=on")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0036"
                    "执行结束==")
