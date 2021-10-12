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
Case Name   : 1主2备，备机上执行gs_dropnode 期望:合理报错，退出执行
Description :
        1.1主2备，备机执行减容
Expect      :
        1.期望:操作成功，减容成功
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
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0021 start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")
        self.s_node1 = Node("Standby1DbUser")
        self.s_node2 = Node("Standby2DbUser")

    def test_tool(self):
        LOGGER.info("步骤1：1主2备，执行减容 根据减容和重启提示输入yes")
        result = COMMONSH.execut_db_sql(
            "select count(*) from pg_stat_get_wal_senders();")
        LOGGER.info(result)
        self.assertEqual("2", result.split("\n")[-2].strip())
        execute_cmd = f'''source {macro.DB_ENV_PATH};
                    expect <<EOF
                    set timeout 120
                    spawn gs_dropnode -U {self.user_node.ssh_user} \
                    -G {self.user_node.ssh_user} \
                    -h {self.s_node2.ssh_host}
                    expect eof\n''' + '''EOF'''
        LOGGER.info(execute_cmd)
        result = self.s_node1.sh(execute_cmd).result()
        LOGGER.info(result)
        self.assertIn("can only be executed at the primary node", result)

        LOGGER.info("核对减容成功 剩余1+1")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        result = COMMONSH.execut_db_sql(
            "select count(*) from pg_stat_get_wal_senders();")
        LOGGER.info(result)
        self.assertEqual("2", result.split("\n")[-2].strip())

    def tearDown(self):
        LOGGER.info("无需恢复环境")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0021 finish=")
