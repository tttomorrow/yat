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
Case Name   : 减容后执行failover/switchover
Description :
        1.1主2备环境正常，在备1进行switchover 刷新配置文件后重启
        2.原主机现备机进行对当前节点 进行减容
        3.恢复环境
Expect      :
        1.期望：切换成功，重启成功，主备切换成功
        2.期望：合理报错
        3.恢复环境
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
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0044 start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")
        self.s_node1 = Node("Standby1DbUser")
        self.s_node2 = Node("Standby2DbUser")
        self.com_s1 = CommonSH("Standby1DbUser")

    def test_tool(self):
        LOGGER.info("步骤1:1主2备，执行减容 根据减容和重启提示输入yes")
        result = COMMONSH.execut_db_sql(
            "select count(*) from pg_stat_get_wal_senders();")
        LOGGER.info(result)
        self.assertEqual("2", result.split("\n")[-2].strip())

        LOGGER.info("步骤1:执行switchover")
        result = self.com_s1.execute_gsctl("switchover",
                                           "switchover completed")
        LOGGER.info(result)
        self.assertTrue(result)

        LOGGER.info("刷新配置文件，重启检查数据库集群状态")
        result = self.s_node1.sh(
            f"source {macro.DB_ENV_PATH};gs_om -t refreshconf").result()
        LOGGER.info(result)
        self.assertIn("Successfully generated dynamic configuration file",
                      result)
        result = self.com_s1.restart_db_cluster()
        LOGGER.info(result)
        status = self.com_s1.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertIn("P Standby Normal", status)
        self.assertIn("S Primary Normal", status)
        self.assertTrue("Normal" in status or "Degraded" in status)

        execute_cmd = f'''source {macro.DB_ENV_PATH};
                    expect <<EOF
                    set timeout 120
                    spawn gs_dropnode -U {self.user_node.ssh_user} \
                    -G {self.user_node.ssh_user} \
                    -h {self.s_node1.ssh_host}
                    expect eof\n''' + '''EOF'''
        LOGGER.info(execute_cmd)
        result = self.user_node.sh(execute_cmd).result()
        LOGGER.info(result)
        self.assertIn("can only be executed at the primary node", result)

        LOGGER.info("核对减容失败 剩余1+2")
        status = self.com_s1.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        result = self.com_s1.execut_db_sql(
            "select count(*) from pg_stat_get_wal_senders();")
        LOGGER.info(result)
        self.assertEqual("2", result.split("\n")[-2].strip())

    def tearDown(self):
        LOGGER.info("步骤3:恢复环境")
        LOGGER.info("查看主备是否正常")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        if "P Standby" in status or "S Primary" in status:
            result = COMMONSH.execute_gsctl("switchover",
                                            "switchover completed")
            LOGGER.info(result)
            LOGGER.info("刷新配置文件")
            result = self.user_node.sh(
                f"source {macro.DB_ENV_PATH};gs_om -t refreshconf").result()
            LOGGER.info(result)
        result = self.com_s1.restart_db_cluster()
        LOGGER.info(result)
        result = COMMONSH.execut_db_sql(
            "select count(*) from pg_stat_get_wal_senders();")
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.assertTrue("S Standby" in status and "P Primary" in status)
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0044 finish=")
