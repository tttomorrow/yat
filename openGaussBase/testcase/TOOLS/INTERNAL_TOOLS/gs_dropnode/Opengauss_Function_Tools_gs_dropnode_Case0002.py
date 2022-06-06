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
Case Type   : gs_dropnode
Case Name   : 1主2备，无参，一参两参，参数大小写不一致 期望:合理报错，退出执行
Description :
        1.无参 期望:合理报错
        2.1参 期望:合理报错
        3.2参 期望:合理报错
        4.3参但参数大小写不一致 期望:合理报错
        5.有参无value，有value无参 期望：合理报错
        6.清理环境
Expect      :
        1.无参 期望:合理报错
        2.1参 期望:合理报错
        3.2参 期望:合理报错
        4.3参但参数大小写不一致 期望:合理报错
        5.有参无value，有value无参 期望：合理报错
        6.清理环境
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


@unittest.skipIf(1 == COMMONSH.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class Gstoolstestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0002 start==")
        self.constant = Constant()
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")
        self.standby_node2 = Node("Standby2DbUser")
        self.temp_file = f"/home/{self.user_node.ssh_user}/test_dropnode.sh"

    def test_tool(self):
        LOGGER.info("步骤1：无参 期望:合理报错")
        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
                                    f"gs_dropnode").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Empty parameter. "
                      "The -U parameter is missing in the command.", sql_cmd)

        LOGGER.info("步骤2：1参 期望:合理报错")
        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -U {self.user_node.ssh_user}").result()
        LOGGER.info(sql_cmd)
        self.assertIn(
            "Empty parameter. The -G parameter is missing in the command.",
            sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -G {self.user_node.ssh_user}").result()
        LOGGER.info(sql_cmd)
        self.assertIn(
            "Empty parameter. The -U parameter is missing in the command.",
            sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -h {self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Empty parameter. "
                      "The -U parameter is missing in the command.", sql_cmd)

        LOGGER.info("步骤3：2参 期望:合理报错")
        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode "
            f"-U {self.user_node.ssh_user} "
            f"-h {self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn(
            "Empty parameter. The -G parameter is missing in the command.",
            sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -G {self.user_node.ssh_user} "
            f"-h {self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn(
            "Empty parameter. The -U parameter is missing in the command.",
            sql_cmd)

        sql_cmd = f'''rm -rf {self.temp_file};\
            echo "source {macro.DB_ENV_PATH}" >> {self.temp_file};\
            echo "gs_dropnode -U {self.user_node.ssh_user} \
            -G {self.user_node.ssh_user}" >> {self.temp_file};\
            chmod +x {self.temp_file};ls {self.temp_file}'''
        LOGGER.info(sql_cmd)
        sql_cmd = self.user_node.sh(sql_cmd).result()
        LOGGER.info(sql_cmd)
        self.assertIn(self.temp_file, sql_cmd)
        sql_cmd = self.user_node.sh(f"sh {self.temp_file}").result()
        LOGGER.info(sql_cmd)
        self.assertIn(
            "Empty parameter. The -h parameter is missing in the command.",
            sql_cmd)

        LOGGER.info("步骤4：3参 期望:合理报错")
        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -u {self.user_node.ssh_user} "
            f"-g {self.user_node.ssh_user} "
            f"-H {self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Unrecognized parameter: -u", sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -U {self.user_node.ssh_user} "
            f"-g {self.user_node.ssh_user} "
            f"-H {self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Unrecognized parameter: -g", sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -U {self.user_node.ssh_user} "
            f"-G {self.user_node.ssh_user} "
            f"-H {self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Unrecognized parameter: -H", sql_cmd)

        LOGGER.info("步骤5：有参无value，有value无参 期望：合理报错")
        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -U {self.user_node.ssh_user} "
            f"{self.user_node.ssh_user} "
            f"{self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Unrecognized parameter", sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -U {self.user_node.ssh_user} "
            f"-G {self.user_node.ssh_user} "
            f"{self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Unrecognized parameter", sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode {self.user_node.ssh_user} "
            f"-G {self.user_node.ssh_user} "
            f"-h {self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Unrecognized parameter", sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
                                    f"gs_dropnode -U -G -h").result()
        LOGGER.info(sql_cmd)
        self.assertIn("option -h requires argument", sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -U {self.user_node.ssh_user} "
            f"-G {self.user_node.ssh_user} -h").result()
        LOGGER.info(sql_cmd)
        self.assertIn("option -h requires argument", sql_cmd)

    def tearDown(self):
        LOGGER.info("步骤6:清理环境")
        sql_cmd = self.user_node.sh(f"rm -rf {self.temp_file}").result()
        LOGGER.info(sql_cmd)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0002 finish=")
