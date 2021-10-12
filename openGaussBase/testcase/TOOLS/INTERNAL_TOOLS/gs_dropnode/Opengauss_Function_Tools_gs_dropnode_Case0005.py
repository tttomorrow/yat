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
Case Name   : 3参，1主2备（按照提示输入否no n NO N） 期望:减容操作失败。集群情况正常
Description :
        1.1主2备，执行减容 根据提示输入no
        2.在主机上检查数据库集群状态。
        3.1主2备，执行减容 根据提示输入n
        4.在主机上检查数据库集群状态。
        5.1主2备，执行减容 根据提示输入NO
        6.在主机上检查数据库集群状态。
        7.1主2备，执行减容 根据提示输入N
        8.在主机上检查数据库集群状态。
Expect      :
        1.期望:操作成功，减容停止
        2.期望:1主2备未减容，wal函数查询为1主2备，local_role显示为Primary，重启后检查再次检查结果一致
        3.期望:操作成功，减容停止
        4.期望:1主2备未减容，wal函数查询为1主2备，local_role显示为Primary，重启后检查再次检查结果一致
        5.期望:操作成功，减容停止
        6.期望:1主2备未减容，wal函数查询为1主2备，local_role显示为Primary，重启后检查再次检查结果一致
        7.期望:操作成功，减容停止
        8.期望:1主2备未减容，wal函数查询为1主2备，local_role显示为Primary，重启后检查再次检查结果一致
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
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0005 start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")
        self.standby_node2 = Node("Standby2DbUser")

    def test_tool(self):
        result = COMMONSH.execut_db_sql("select count(*) from "
                                        "pg_stat_get_wal_senders();")
        LOGGER.info(result)
        self.assertEqual("2", result.split("\n")[-2].strip())

        info_list = ["no", "n", "NO", "N"]
        for i in range(1, 5):
            LOGGER.info(f"步骤{i}：1主2备，执行减容 根据减容和重启提示输入yes")
            execute_cmd = f'''source {macro.DB_ENV_PATH};
                        expect <<EOF 
                        set timeout 120 
                        spawn gs_dropnode -U {self.user_node.ssh_user} \
                        -G {self.user_node.ssh_user} \
                        -h {self.standby_node2.ssh_host}
                        expect "*drop the target node (yes/no)?*" 
                        send "{info_list[i-1]}\\n" 
                        expect eof\n''' + '''EOF'''
            result = self.user_node.sh(execute_cmd).result()
            LOGGER.info(result)
            self.assertIn("Operation aborted", result)

            LOGGER.info(f"步骤{i+1}：核对减容失败")
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
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0005 finish=")
