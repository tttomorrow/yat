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
Case Name   : 修改指定数据库，用户，会话级别的参数unix_socket_permissions
Description : 1、查看unix_socket_permissions默认值；
              source /opt/opengauss810/env
              gs_guc check -D /opt/opengauss810/cluster/dn1
              -c unix_socket_permissions
              2、在gsql中分别设置数据库、用户、会话、级别
              unix_socket_permissions；
              alter database postgres set unix_socket_permissions to 0750;
              alter user env109 set unix_socket_permissions to 0750;
              set unix_socket_permissions to 0750;
Expect      : 1、显示默认值；
              2、参数修改失败；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

COMMONSH = CommonSH('PrimaryDbUser')


class Deletaduit(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Connectionauthentication_Case0107.py start==')
        self.rootNode = Node()
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        result = COMMONSH.execute_gsguc('check', '0700',
                                       'unix_socket_permissions')
        self.assertTrue(result)
        self.log.info("设置unix_socket_permissions，校验预期结果")
        sql_cmd = COMMONSH.execut_db_sql(
            f'''alter database postgres \
            set unix_socket_permissions to 0750;''')
        self.log.info(sql_cmd)
        self.assertIn("ERROR", sql_cmd)
        sql_cmd1 = COMMONSH.execut_db_sql(
            f'''alter user {self.dbUserNode1.db_user} \
            set unix_socket_permissions to 0750;''')
        self.log.info(sql_cmd1)
        self.assertIn("ERROR", sql_cmd1)
        sql_cmd2 = COMMONSH.execut_db_sql(
            f'''set unix_socket_permissions to 0750;''')
        self.log.info(sql_cmd2)
        self.assertIn("ERROR", sql_cmd2)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'unix_socket_permissions=\'0700\'')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0107.py finish==')
