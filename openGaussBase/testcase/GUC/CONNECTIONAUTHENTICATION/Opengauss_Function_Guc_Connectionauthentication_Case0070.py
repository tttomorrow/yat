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
Case Name   : sysadmin_reserved_connections参数gs_guc set设置为其他数据类型
Description : 1、查看sysadmin_reserved_connections默认值；
              2、gs_guc set设置sysadmin_reserved_connections为其他数据类型
Expect      : 1、显示默认值；
              2、参数修改失败；
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
        self.log.info('==Connectionauthentication_Case0070.py start==')
        self.rootNode = Node()
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_startdb(self):
        self.log.info("查看sysadmin_reserved_connections默认值，并校验；")
        result = COMMONSH.execut_db_sql('show sysadmin_reserved_connections;')
        self.log.info(result)
        self.assertEqual('3', result.split('\n')[2].strip())
        self.log.info("设置sysadmin_reserved_connections为'test',观察预期结果")
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"sysadmin_reserved_connections"
                                        f"='test'")
        self.assertFalse(result)
        self.log.info("设置sysadmin_reserved_connections为-1，观察预期结果")
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'sysadmin_reserved_connections=-1')
        self.assertFalse(result)
        self.log.info("设置sysadmin_reserved_connections为262144,观察预期结果")
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'sysadmin_reserved_connections'
                                        f'=262144')
        self.assertFalse(result)
        self.log.info("设置sysadmin_reserved_connections为小数,观察预期结果")
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'sysadmin_reserved_connections=262.5')
        self.assertFalse(result)
        self.log.info("设置sysadmin_reserved_connections为空值,观察预期结果")
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"sysadmin_reserved_connections=''")
        self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execut_db_sql('show sysadmin_reserved_connections;')
        self.log.info(result)
        if '3' != result.split('\n')[2].strip():
            result = COMMONSH.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'sysadmin_reserved_connections=3')
            self.assertTrue(result)
            msg = COMMONSH.restart_db_cluster()
            self.log.info(msg)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0070.py finish==')
