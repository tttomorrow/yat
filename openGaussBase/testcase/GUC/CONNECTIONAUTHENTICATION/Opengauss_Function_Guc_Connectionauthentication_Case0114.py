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
Case Name   : 使用ALTER SYSTEM SET修改数据库参数unix_socket_permissions为空值
Description : 1、查看unix_socket_permissions默认值；
              source /opt/opengauss810/env
              gs_guc check -D /opt/opengauss810/cluster/dn1
              -c unix_socket_permissions
              2、使用ALTER SYSTM SET修改参数unix_socket_permissions为空值;
              ALTER SYSTEM set unix_socket_permissions to ' ';
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
        self.log.info('==Connectionauthentication_Case0114.py start==')
        self.rootNode = Node()
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        result = COMMONSH.execute_gsguc('check', '0700',
                                       'unix_socket_permissions')
        self.assertTrue(result)
        self.log.info("设置unix_socket_permissions为空值")
        sql_cmd = COMMONSH.execut_db_sql(
            f'''ALTER SYSTEM set unix_socket_permissions to ' ';''')
        self.log.info(sql_cmd)
        self.assertIn("ERROR", sql_cmd)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'unix_socket_permissions=\'0700\'')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0114.py finish==')
