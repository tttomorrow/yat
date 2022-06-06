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
Case Name   : unix_socket_group参数使用gs_guc reload设置
Description : 1、查看unix_socket_group默认值；
              2、使用设置gs_guc reload设置unix_socket_group
              gs_guc reload -D /opt/opengauss810/cluster/dn1
              -c "unix_socket_group='env109'"
              3、校验是否修改成功；
              show unix_socket_group;
              4、恢复默认值
Expect      : 1、显示默认值；
              2、参数修改成功；
              3、参数值保持默认，gs_guc reload方法设置不生效；
              4、修改成功；
"""

import unittest

from yat.test import Node

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

COMMONSH = CommonSH('PrimaryDbUser')


class Deletaduit(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Connectionauthentication_Case0095.py start==')
        self.rootNode = Node()
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        sql_cmd = COMMONSH.execut_db_sql('show unix_socket_group;')
        self.log.info(sql_cmd)
        self.assertIn('', sql_cmd)
        self.log.info("设置unix_socket_group")
        result = COMMONSH.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"unix_socket_group='test'")
        self.assertTrue(result)
        self.log.info("校验参数是否修改成功")
        sql_cmd = COMMONSH.execut_db_sql('show unix_socket_group;')
        self.log.info(sql_cmd)
        self.assertIn('', sql_cmd)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"unix_socket_group=''")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0095.py finish==')
