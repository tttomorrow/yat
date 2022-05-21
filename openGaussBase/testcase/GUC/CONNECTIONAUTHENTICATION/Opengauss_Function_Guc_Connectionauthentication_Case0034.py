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
Case Type   : GUC
Case Name   : 使用alter system set修改参数local_bind_address为非字符类型
Description : 1、查看local_bind_address默认值；
              source env
              show local_bind_address;
              2、使用alter system set修改参数local_bind_address;为非字符类型
              alter system set  local_bind_address to 123456;
              3、重启数据库使其生效，观察预期结果
              gs_om -t stop && gs_om -t start
              4、恢复默认值
Expect      : 1、显示默认值；
              2、参数修改成功；
              3、重启成功；
              4、恢复默认值成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

COMMONSH = CommonSH("PrimaryDbUser")


class Guctestcase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.name = "Opengauss_Function_Guc_Connectionauthentication_Case0034"
        self.log.info(f"=={self.name}.py start==")
        self.dbUserNode1 = Node(node="PrimaryDbUser")
        self.ipadd = self.dbUserNode1.db_host

    def test_guc(self):
        self.log.info("步骤1：查询该参数默认值")
        sql_cmd = COMMONSH.execut_db_sql("show local_bind_address;")
        self.log.info(sql_cmd)
        self.assertIn(self.ipadd, sql_cmd)

        self.log.info("步骤2：alter system set设置"
                      "local_bind_address为非字符类型")
        sql_cmd = COMMONSH.execut_db_sql(
            "alter system set local_bind_address to 12345;")
        self.log.info(sql_cmd)
        self.assertIn("ALTER SYSTEM SET", sql_cmd)

        self.log.info("步骤3：重启数据库使其生效,预期成功")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def tearDown(self):
        self.log.info("步骤4：恢复为本机ip")
        sql_cmd = COMMONSH.execut_db_sql("show local_bind_address;")
        self.log.info(sql_cmd)
        if str(self.ipadd) != sql_cmd.splitlines()[-2].strip():
            sql_cmd = COMMONSH.execut_db_sql(
                f"alter system set local_bind_address to '{self.ipadd}';")
            self.log.info(sql_cmd)
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(f"=={self.name}.py finish==")
