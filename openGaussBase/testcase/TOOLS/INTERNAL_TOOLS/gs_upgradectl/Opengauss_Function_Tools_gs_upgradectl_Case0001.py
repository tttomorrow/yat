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
Case Type   : gs_upgradectl
Case Name   : gs_upgradectl 基础命令
Description :
    1.集群状态Normal，在root用户下执行预安装
    2.gs_upgradectl -? | gs_upgradectl --help
    3.gs_upgradectl -V | gs_upgradectl --version
    4.gs_upgradectl -t chose-strategy
    5.gs_upgradectl -？ | gs_upgradectl -help
    6.gs_upgradectl -v | gs_upgradectl -version
Expect      :
    1.预安装成功 gs_om -V显示为升级后版本
    2.显示帮助信息
    3.显示gs_upgradectl版本信息
    4.无法-查询失败
    5.合理报错
    6.合理报错
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


class Gstoolstestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("Opengauss_Function_Tools_gs_upgradectl_Case0001 start")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")

    def test_tool(self):
        LOGGER.info("步骤1：预安装pass")
        LOGGER.info("步骤2：gs_upgradectl -? | gs_upgradectl --help")
        cmd_list = ["gs_upgradectl -?", "gs_upgradectl --help"]
        for cmd in cmd_list:
            result = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
                                       f"{cmd}").result()
            LOGGER.info(result)
            LOGGER.info("语法核对")
            con_list = ["gs_upgradectl is a utility to upgrade a cluster",
                        "gs_upgradectl -? | --help",
                        "gs_upgradectl -V | --version",
                        "gs_upgradectl -t chose-strategy [-l LOGFILE]",
                        "gs_upgradectl -t commit-upgrade "
                        "-X XMLFILE [-l LOGFILE]",
                        "gs_upgradectl -t auto-upgrade -X XMLFILE "
                        "[-l LOGFILE] [--grey]",
                        "gs_upgradectl -t auto-rollback -X XMLFILE "
                        "[-l LOGFILE] [--force]"]
            for con in con_list:
                self.assertIn(con, result)
            LOGGER.info("参数核对")
            con_list = ["-?, --help", "-V, --version", "-t", "-X", "--force",
                        "--grey"]
            for con in con_list:
                self.assertIn(con, result)

        LOGGER.info("步骤3：gs_upgradectl -V | gs_upgradectl --version")
        cmd_list = ["gs_upgradectl -V", "gs_upgradectl --version"]
        for cmd in cmd_list:
            result = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
                                       f"{cmd}").result()
            LOGGER.info(result)
            LOGGER.info("语法核对")
            self.assertIn("gs_upgradectl", result)
            self.assertIn("compiled at", result)
            self.assertNotIn("bash", result)
            self.assertNotIn("ERROR", result)
            self.assertNotIn("failed", result)

        LOGGER.info("步骤4：gs_upgradectl -t chose-strategy")
        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_upgradectl -t chose-strategy").result()
        LOGGER.info(sql_cmd)
        self.assertIn("New cluster commitid cannot be "
                      "same with old cluster commitid.. Do nothing this time",
                      sql_cmd)
        self.assertIn("Failed to upgrade strategy", sql_cmd)

        LOGGER.info("步骤5-6：参数错误 合理报错")
        cmd_list = ["gs_upgradectl -？", "gs_upgradectl -help",
                    "gs_upgradectl -v", "gs_upgradectl -version"]
        for cmd in cmd_list:
            result = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
                                       f"{cmd}").result()
            LOGGER.info(result)
            self.assertIn("GAUSS-50001", result)
            self.assertIn("Incorrect parameter", result)
            self.assertIn("Parameter '-t' is required", result)

    def tearDown(self):
        LOGGER.info("步骤6:无需恢复")
        status = COMMONSH.get_db_cluster_status("detail")
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("Opengauss_Function_Tools_gs_upgradectl_Case0001 finish")
