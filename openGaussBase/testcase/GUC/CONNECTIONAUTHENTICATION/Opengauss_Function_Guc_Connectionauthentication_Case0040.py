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
Case Name   : 修改指定数据库，用户，会话级别的参数max_connections
Description : 1、查看max_connections默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c max_connections
              2、在gsql中分别设置数据库、用户、会话、级别
              max_connections（不可小于等于max_wal_senders）；
              alter database postgres set max_connections to 55810;
              alter user {self.dbUserNode1.db_user}
              set max_connections to 55810;
              set max_connections to 55810;
Expect      : 1、显示默认值；
              2、参数修改失败；
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
        self.log.info("==Connectionauthentication_Case0040.py start==")
        self.rootNode = Node()
        self.dbUserNode1 = Node(node="PrimaryDbUser")

    def test_guc(self):
        self.log.info("查看max_connections默认值，并校验；")
        result = COMMONSH.execute_gsguc("check", 
                                        "5000", 
                                        "max_connections")
        self.assertTrue(result)

        sql_cmd = COMMONSH.execut_db_sql("show max_wal_senders;")
        self.log.info(sql_cmd)
        self.defaultWalSenders = sql_cmd.split("\n")[-2].strip()

        self.log.info("设置max_wal_senders参数，"
                      "并据此设置max_connections，校验预期结果")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"max_wal_senders=4")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        sql_cmd = COMMONSH.execut_db_sql(f"alter database postgres "
            f"set max_connections to '55810';")
        self.log.info(sql_cmd)
        self.assertIn("ERROR", sql_cmd)
        sql_cmd1 = COMMONSH.execut_db_sql(f"alter user "
            f"{self.dbUserNode1.db_user} "
            f"set max_connections to '55810';")
        self.log.info(sql_cmd1)
        self.assertIn("ERROR", sql_cmd1)
        sql_cmd2 = COMMONSH.execut_db_sql(f"set max_connections to '55810';")
        self.log.info(sql_cmd2)
        self.assertIn("ERROR", sql_cmd2)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"max_wal_senders="
                                        f"{self.defaultWalSenders}")
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"max_connections=5000")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info("==Connectionauthentication_Case0040.py finish==")
