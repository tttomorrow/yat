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
Case Type   : gs_dropnode
Case Name   : 1主2备host参数为主机ip，非集群ip，错误ip，多个ip间连接符错误 期望:合理报错，退出执行
Description :
        1.host参数为主机ip 期望:合理报错
        2.host参数为非集群ip 期望:合理报错
        3.host参数为错误ip 期望:合理报错
        4.host参数为2备机ip,连接符错误 期望:合理报错
        5.空格错误 期望:合理报错
        6.清理环境
Expect      :
        1.host参数为主机ip 期望:合理报错
        2.host参数为非集群ip 期望:合理报错
        3.host参数为错误ip 期望:合理报错
        4.host参数为2备机ip,连接符错误 期望:合理报错
        5.空格错误 期望:合理报错
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
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0003 start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")
        self.standby_node1 = Node("Standby1DbUser")
        self.standby_node2 = Node("Standby2DbUser")
        self.temp_file = f"/home/{self.user_node.ssh_user}/test_dropnode.sh"
        self.hostip = "1.2.3.4"

    def test_tool(self):
        LOGGER.info("步骤1：host参数为主机ip 期望:合理报错")
        sql_cmd = f'''rm -rf {self.temp_file};\
            echo "source {macro.DB_ENV_PATH}" >> {self.temp_file};\
            echo "gs_dropnode -U {self.user_node.ssh_user} \
            -G {self.user_node.ssh_user} -h {self.user_node.ssh_host}" \
            >> {self.temp_file};\
            chmod +x {self.temp_file};\
            ls {self.temp_file}'''
        LOGGER.info(sql_cmd)
        sql_cmd = self.user_node.sh(sql_cmd).result()
        LOGGER.info(sql_cmd)
        self.assertIn(self.temp_file, sql_cmd)
        sql_cmd = self.user_node.sh(f"sh {self.temp_file}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Can not drop local host", sql_cmd)

        LOGGER.info("步骤2：host参数为非集群ip 期望:合理报错")
        sql_cmd = f'''rm -rf {self.temp_file};\
            echo "source {macro.DB_ENV_PATH}" >> {self.temp_file};\
            echo "gs_dropnode -U {self.user_node.ssh_user} \
            -G {self.user_node.ssh_user} \
            -h {self.hostip}" >> {self.temp_file};\
            chmod +x {self.temp_file};ls {self.temp_file}'''
        LOGGER.info(sql_cmd)
        sql_cmd = self.user_node.sh(sql_cmd).result()
        LOGGER.info(sql_cmd)
        self.assertIn(self.temp_file, sql_cmd)
        sql_cmd = self.user_node.sh(f"sh {self.temp_file}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("not in the current cluster", sql_cmd)

        LOGGER.info("步骤3：host参数为错误ip 期望:合理报错")
        ip_list = ["10.28.21.256", "10.28.21.a", "10.28.21.=", "10.28.21.F1"]
        for ip in ip_list:
            sql_cmd = f'''rm -rf {self.temp_file};\
                echo "source {macro.DB_ENV_PATH}" >> {self.temp_file};\
                echo "gs_dropnode -U {self.user_node.ssh_user} \
                -G {self.user_node.ssh_user} -h {ip}" >> {self.temp_file};\
                chmod +x {self.temp_file};ls {self.temp_file}'''
            LOGGER.info(sql_cmd)
            sql_cmd = self.user_node.sh(sql_cmd).result()
            LOGGER.info(sql_cmd)
            self.assertIn(self.temp_file, sql_cmd)
            sql_cmd = self.user_node.sh(f"sh {self.temp_file}").result()
            LOGGER.info(sql_cmd)
            self.assertIn("not in the current cluster", sql_cmd)

        LOGGER.info("步骤4：2备机ip,连接符错误 期望:合理报错")
        ip_list = [
            f"{self.standby_node1.ssh_host}，{self.standby_node2.ssh_host}",
            f"{self.standby_node1.ssh_host}{self.standby_node2.ssh_host}",
            f"{self.standby_node1.ssh_host}+{self.standby_node2.ssh_host}",
            f"{self.standby_node1.ssh_host}-{self.standby_node2.ssh_host}"]
        for ip in ip_list:
            sql_cmd = f'''rm -rf {self.temp_file};\
                echo "source {macro.DB_ENV_PATH}" >> {self.temp_file};\
                echo "gs_dropnode -U {self.user_node.ssh_user} \
                -G {self.user_node.ssh_user} -h {ip}" >> {self.temp_file};\
                chmod +x {self.temp_file};ls {self.temp_file}'''
            LOGGER.info(sql_cmd)
            sql_cmd = self.user_node.sh(sql_cmd).result()
            LOGGER.info(sql_cmd)
            self.assertIn(self.temp_file, sql_cmd)
            sql_cmd = self.user_node.sh(f"sh {self.temp_file}").result()
            LOGGER.info(sql_cmd)
            self.assertIn("not in the current cluster", sql_cmd)

        LOGGER.info("步骤5：空格错误 期望:合理报错")
        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode-U {self.user_node.ssh_user} "
            f"-G {self.user_node.ssh_user} "
            f"-h {self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("gs_dropnode-U", sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -U {self.user_node.ssh_user}"
            f"-G {self.user_node.ssh_user} "
            f"-h {self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Unrecognized parameter", sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -U {self.user_node.ssh_user}"
            f"-G {self.user_node.ssh_user}"
            f"-h {self.standby_node2.ssh_host}").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Unrecognized parameter", sql_cmd)

        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_dropnode -U {self.user_node.ssh_user}"
            f"-G {self.user_node.ssh_user}"
            f"-h {self.standby_node2.ssh_host},").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Unrecognized parameter", sql_cmd)

    def tearDown(self):
        LOGGER.info("步骤6:清理环境")
        sql_cmd = self.user_node.sh(f"rm -rf {self.temp_file}").result()
        LOGGER.info(sql_cmd)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0003 finish=")
