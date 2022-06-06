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
Case Name   : 3参，1主2备（按照提示输入是和否之外的无效值） 期望:减容操作失败。节点情况正常
Description :
        1.1主2备，执行减容 根据提示输入aaa
        2.在主机上检查数据库集群状态。
Expect      :
        1.期望:提示输入错误，减容停止
        2.期望:1主2备未减容
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
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0006 start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")
        self.standby_node2 = Node("Standby2DbUser")

    def test_tool(self):
        LOGGER.info("步骤1：1主2备，执行减容 根据减容和重启提示输入错误值")
        con_list = ["test", "1", "0", "==", "!!", " ", "2.5", "ye", "ye s"]
        for con in con_list:
            execute_cmd = f'''source {macro.DB_ENV_PATH};
                        expect <<EOF 
                        set timeout 120 
                        spawn gs_dropnode -U {self.user_node.ssh_user} \
                        -G {self.user_node.ssh_user} \
                        -h {self.standby_node2.ssh_host}
                        expect "*drop the target node (yes/no)?*" 
                        send "{con}\\n" 
                        expect "*Please type 'yes' or 'no':*" 
                        send "{con}\\n" 
                        expect "*Please type 'yes' or 'no':*" 
                        send "{con}\\n" 
                        expect eof\n''' + '''EOF'''
            LOGGER.info(execute_cmd)
            result = self.user_node.sh(execute_cmd).result()
            LOGGER.info(result)
            self.assertIn("Operation aborted", result)

            LOGGER.info("步骤2：核对减容失败")
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
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0006 finish=")
