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
Case Name   : set修改参数unix_socket_group为test0104
Description :
    1、查看unix_socket_group和listen_addresses默认值；
    show listen_addresses;
    show unix_socket_group;
    2、root用户创建group
    groupdel test0104;groupadd test0104;
    3、使用设置gs_guc set设置unix_socket_group 重启
    gs_guc set -N all  -D all -c "unix_socket_group='test0104'"
    gs_om -t stop;gs_om -t start
    4、恢复默认值
    groupdel test0104;
    gs_guc set -N all -D all -c "unix_socket_group=''"
Expect      :
    1、查看unix_socket_group默认值
    2、root用户创建group成功
    3、设置成功，重启失败
    4、恢复默认值
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class Guctestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0104"
            " start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")
        self.root_node = Node("PrimaryRoot")

    def test_guc(self):
        LOGGER.info("步骤1：查询unix_socket_group 期望：默认值空")
        sql_cmd = COMMONSH.execut_db_sql("show unix_socket_directory;")
        LOGGER.info(sql_cmd)
        self.socket_path = sql_cmd.split("\n")[-2].strip()
        sql_cmd = COMMONSH.execut_db_sql("show unix_socket_group;")
        LOGGER.info(sql_cmd)
        self.assertEqual("", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("步骤2:root用户创建group")
        result = self.root_node.sh(f"groupadd test0104;"
                                   f"chown -R "
                                   f"{self.user_node.ssh_user}:test0104 "
                                   f"{self.socket_path}").result()
        LOGGER.info(result)
        self.assertNotIn("bash", result)

        LOGGER.info("步骤3:修改unix_socket_group为test0104等，期望：修改成功重启失败")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "unix_socket_group='test0104'")
        self.assertTrue(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        self.assertFalse(result)

    def tearDown(self):
        LOGGER.info("步骤4:恢复默认值")
        result = self.root_node.sh(f"groupdel test0104;"
                                   f"chown -R "
                                   f"{self.user_node.ssh_user}:"
                                   f"{self.user_node.ssh_user} "
                                   f"{self.socket_path}").result()
        LOGGER.info(result)
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"unix_socket_group=''")
        LOGGER.info(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0104"
            " finish==")
