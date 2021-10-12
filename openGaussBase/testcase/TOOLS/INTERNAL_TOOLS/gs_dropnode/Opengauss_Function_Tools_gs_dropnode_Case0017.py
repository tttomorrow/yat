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
Case Name   : gs_dropnode -?, –help -V, –version 期望:显示参数信息和版本信息
Description :
        1.执行如下语句，显示参数信息
        gs_dropnode --help
        gs_dropnode -?
        2.执行如下语句，显示版本信息
        gs_dropnode --version
        gs_dropnode -V
Expect      :
        1.期望:显示参数信息
        2.期望:显示版本信息
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
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0017 start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")

    def test_tool(self):
        LOGGER.info("步骤1：执行如下语句，显示参数信息")
        cmd_list = ["gs_dropnode --help", "gs_dropnode -?"]
        for cmd in cmd_list:
            result = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
                                       f"{cmd}").result()
            LOGGER.info(result)
            LOGGER.info("语法核对")
            con_list = ["gs_dropnode -? | --help",
                        "gs_dropnode -V | --version",
                        "gs_dropnode -U USER -G GROUP -h nodeList"]
            for con in con_list:
                self.assertIn(con, result)
            LOGGER.info("参数核对")
            con_list = ["-U", "-G", "-h", "-?, --help", "-V, --version"]
            for con in con_list:
                self.assertIn(con, result)

        LOGGER.info("步骤2：执行如下语句，显示版本信息")
        cmd_list = ["gs_dropnode --version", "gs_dropnode -V"]
        for cmd in cmd_list:
            result = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
                                       f"{cmd}").result()
            LOGGER.info(result)
            self.assertIn("gs_dropnode", result)
            self.assertIn("openGauss", result)

    def tearDown(self):
        LOGGER.info("无需恢复环境")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Tools_gs_dropnode_Case0017 finish=")
