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
Case Type   : GUC
Case Name   : reload修改参数application_name为dn1_6001
Description :
    1、查看application_name默认值；
    cat {postgresql.conf} | grep 'application_name ='
    2、使用设置gs_guc reload设置application_name
    gs_guc reload -N all  -D all -c "application_name='dn1_6001'"
    3、在相应配置文件中查看配置
    cat {postgresql.conf} | grep 'application_name ='
    4、恢复默认值
Expect      :
    1、查看application_name默认值
    2、修改application_name为dn1_6001 reload成功
    3、查看配置为dn1_6001
    4、恢复默认值
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


class Guctestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0117"
            " start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")
        self.conf_file = f"{macro.DB_INSTANCE_PATH}/{macro.DB_PG_CONFIG_NAME}"

    def test_guc(self):
        LOGGER.info("步骤1：查询application_name 期望：默认值空")
        result = self.user_node.sh(f"cat {self.conf_file} | "
                                   f"grep 'application_name ='").result()
        LOGGER.info(result)
        self.default_value = result.split("=")[-1].strip()

        LOGGER.info("步骤2:修改application_name为abc等，期望：修改失败，show参数为默认值")
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "application_name='dn1_6001'",
                                        node_name=f"{self.user_node}",
                                        single=True)
        self.assertTrue(result)

        result = self.user_node.sh(f"cat {self.conf_file} | "
                                   f"grep 'application_name ='").result()
        LOGGER.info(result)
        self.assertIn("dn1_6001", result.split("=")[-1].strip())

    def tearDown(self):
        LOGGER.info("步骤3:恢复默认值,由驱动连接的时候自动设置,无需恢复")
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"application_name="
                                        f"{self.default_value}",
                                        node_name=f"{self.user_node}",
                                        single=True)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0117"
            " finish==")
