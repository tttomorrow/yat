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
Case Name   : 减容用户为不存在的用户，root用户，和非初始用户 期望：合理报错 退出执行
Description :
        1.1主2备，减容用户为不存在的用户
        2.1主2备，减容用户为root
        3.1主2备，减容用户为非初始用户
Expect      :
        1.期望：合理报错 退出执行
        2.期望：合理报错 退出执行
        3.期望：合理报错 退出执行
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
COMMONSHROOT = CommonSH("PrimaryRoot")


@unittest.skipIf(1 == COMMONSH.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class Gstoolstestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0038 start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.root_node = Node("PrimaryRoot")
        self.user_node = Node("PrimaryDbUser")
        self.s_node1 = Node("Standby1DbUser")
        self.s_node2 = Node("Standby2DbUser")
        self.temp_file = f"/home/{self.user_node.ssh_user}/temp38.sh"

    def test_tool(self):
        LOGGER.info("步骤1：减容用户为不存在的用户")
        result = COMMONSH.execut_db_sql(
            "select count(*) from pg_stat_get_wal_senders();")
        LOGGER.info(result)
        self.assertEqual("2", result.split("\n")[-2].strip())
        result = self.user_node.sh(f'''rm -rf {self.temp_file};\
            echo "source {macro.DB_ENV_PATH};" >> {self.temp_file};\
            echo "gs_dropnode -U notExist -G notExist \
            -h {self.s_node2.ssh_host}" >> {self.temp_file}''').result()
        LOGGER.info(result)
        self.assertNotIn("bash", result)
        result = self.user_node.sh(f"sh {self.temp_file}").result()
        LOGGER.info(result)
        self.assertIn("User notExist does not exist", result)

        LOGGER.info("步骤2：减容用户为root")
        result = self.user_node.sh(f'''rm -rf {self.temp_file};\
            echo "source {macro.DB_ENV_PATH};" >> {self.temp_file};\
            echo "gs_dropnode -U root -G root \
            -h {self.s_node2.ssh_host}" >> {self.temp_file}''').result()
        LOGGER.info(result)
        self.assertNotIn("bash", result)
        result = self.user_node.sh(f"sh {self.temp_file}").result()
        LOGGER.info(result)
        self.assertIn("not the cluster installation user", result)

        LOGGER.info("步骤3：减容用户为非初始用户")
        result = self.root_node.sh("groupadd dropnode38;"
                                   "useradd -g dropnode38 dropnode38;"
                                   "ls /home").result()
        LOGGER.info(result)
        self.assertIn("dropnode38", result)
        self.assertNotIn("bash", result)

        result = self.user_node.sh(f'''rm -rf {self.temp_file};\
            echo "source {macro.DB_ENV_PATH};" >> {self.temp_file};\
            echo "gs_dropnode -U dropnode38 -G dropnode38 \
            -h {self.s_node2.ssh_host}" >> {self.temp_file}''').result()
        LOGGER.info(result)
        self.assertNotIn("bash", result)
        result = self.user_node.sh(f"sh {self.temp_file}").result()
        LOGGER.info(result)
        self.assertIn("not the cluster installation user", result)

        LOGGER.info("核对减容失败 剩余1+2")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        result = COMMONSH.execut_db_sql(
            "select count(*) from pg_stat_get_wal_senders();")
        LOGGER.info(result)
        self.assertEqual("2", result.split("\n")[-2].strip())

    def tearDown(self):
        LOGGER.info("步骤4：恢复环境")
        result = self.root_node.sh(f"rm -rf {self.temp_file};"
            f"userdel -r dropnode38;ls /home;ls {self.temp_file}").result()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.assertIn("No such file or directory", result)
        self.assertNotIn("dropnode38", result)
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0038 finish=")
