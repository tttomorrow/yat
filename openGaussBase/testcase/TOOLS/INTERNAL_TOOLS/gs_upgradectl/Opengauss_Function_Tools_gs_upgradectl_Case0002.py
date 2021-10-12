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
Case Name   : 灰度升级-X -l指定错误
Description :
    1.集群状态Normal，在root用户下执行预安装
    2.升级指定错误不存在的xml，无权限的文件等
    gs_upgradectl -t auto-upgrade -X {xml2} --grey
    3.root 用户创建文件夹/upgrade
    mkdir /upgrade
    4.gs_upgradectl -t auto-upgrade -X {xml}--grey -l /upgrade/upgrade.log
    5.root 用户清理文件夹/upgrade
    rm -rf /upgrade
Expect      :
    1.预安装成功 gs_om -V显示为升级后版本
    2.合理报错
    3.创建成功
    4.升级失败 合理报错
    5.清理成功
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
        LOGGER.info("Opengauss_Function_Tools_gs_upgradectl_Case0002 start")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")
        self.root_node = Node("PrimaryRoot")
        self.temp_file = f"/home/{self.user_node.ssh_user}/temp.xml"
        self.test_file = f"/home/{self.user_node.ssh_user}/test.sh"
        self.temp_path = f"/home/{self.user_node.ssh_user}/temp.xml"

    def test_tool(self):
        LOGGER.info("步骤1：预安装pass")
        LOGGER.info("步骤2：升级指定错误不存在的xml，无权限的文件等")
        LOGGER.info("指定不存在的xml")
        result = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_upgradectl -t auto-upgrade -X noexists.xml").result()
        LOGGER.info(result)
        self.assertIn("GAUSS-50201", result)
        self.assertIn("does not exist", result)
        LOGGER.info("指定不存在的xml")
        result = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_upgradectl -t auto-upgrade -X noexists.xml --grey").result()
        LOGGER.info(result)
        self.assertIn("GAUSS-50201", result)
        self.assertIn("does not exist", result)

        LOGGER.info("root用户复制xml")
        result = self.root_node.sh(f"rm -rf {self.temp_file};"
           f"cp {macro.DB_XML_PATH} {self.temp_file};"
           f"ls {self.temp_file};chmod 400 {self.temp_file}").result()
        LOGGER.info(result)
        self.assertIn(self.temp_file, result)

        LOGGER.info("指定权限不足的xml")
        result = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_upgradectl -t auto-upgrade -X {self.temp_file}").result()
        LOGGER.info(result)
        self.assertIn("not readable for the user", result)
        self.assertIn(self.constant.PERMISSION_DENY_MSG, result)

        LOGGER.info("指定权限不足的xml")
        result = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_upgradectl -t auto-upgrade "
            f"-X {self.temp_file} --grey").result()
        LOGGER.info(result)
        self.assertIn("not readable for the user", result)
        self.assertIn(self.constant.PERMISSION_DENY_MSG, result)

        LOGGER.info("步骤3：root 用户创建文件夹")
        result = self.root_node.sh(f"rm -rf {self.temp_path};"
            f"mkdir {self.temp_path};ls {self.temp_path}/../;"
            f"chmod 400 {self.temp_path}").result()
        LOGGER.info(result)
        self.assertNotIn("No such file or directory", result)

        LOGGER.info("步骤4：升级指定log")
        sql_cmd = self.user_node.sh(f"source {macro.DB_ENV_PATH};"
            f"gs_upgradectl -t auto-upgrade "
            f"-X {macro.DB_XML_PATH} --grey "
            f"-l {self.temp_path}/upgrade.log").result()
        LOGGER.info(sql_cmd)
        self.assertIn("Permission denied", sql_cmd)

    def tearDown(self):
        LOGGER.info("步骤5:清理环境")
        result = self.root_node.sh(f"rm -rf {self.temp_file};"
                                   f"rm -rf {self.temp_file};"
                                   f"rm -rf {self.test_file};").result()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status("detail")
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("Opengauss_Function_Tools_gs_upgradectl_Case0002 finish")
