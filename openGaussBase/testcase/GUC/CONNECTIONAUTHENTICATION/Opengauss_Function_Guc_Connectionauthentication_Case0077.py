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
Case Name   : sysadmin_reserved_connections参数使用gs_guc reload设置为空值
Description : 1、查看sysadmin_reserved_connections默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c sysadmin_reserved_connections
              2、gs_guc reload设置sysadmin_reserved_connections为超边界值
              gs_guc reload -D {cluster/dn1}
              -c "sysadmin_reserved_connections=' '"
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
        self.log.info('==Connectionauthentication_Case0077.py start==')
        self.rootNode = Node()
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_startdb(self):
        self.log.info("查看sysadmin_reserved_connections默认值并校验；")
        result = COMMONSH.execute_gsguc('check', '3',
                                       'sysadmin_reserved_connections')
        self.assertTrue(result)
        self.log.info("设置sysadmin_reserved_connections为空值")
        result = COMMONSH.execute_gsguc(
            'reload', self.constant.TPCC_ERROR,
            f'sysadmin_reserved_connections=\' \'')
        self.assertTrue(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                        f'sysadmin_reserved_connections=3')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0077.py finish==')
