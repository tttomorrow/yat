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
Case Name   : max_connections参数使用gs_guc set设置为空值
Description : 1、查看max_connections默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c max_connections
              2、使用设置gs_guc set设置max_connections为空值
              gs_guc set -D {cluster/dn1} -c "max_connections=' '"
              gs_guc set -N all  -D {cluster/dn1} -c "max_connections=' '"
Expect      : 1、显示默认值；
              2、参数修改失败；
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

COMMONSH = CommonSH('PrimaryDbUser')


class Deletaduit(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Connectionauthentication_Case0048.py start==')
        self.rootNode = Node()
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        self.dbUserNode = Node(node='PrimaryRoot')
        self.statusCmd = f'source {macro.DB_ENV_PATH};' \
                         f'gs_om -t status --detail'

    def test_startdb(self):
        self.log.info("查看max_connections默认值，并校验；")
        result = COMMONSH.execute_gsguc('check', '5000', 'max_connections')
        self.assertTrue(result)
        self.log.info("设置max_connections为空值，校验预期结果")
        result = COMMONSH.execute_gsguc('set', self.constant.TPCC_ERROR,
                                        f'max_connections=\' \'')
        self.assertTrue(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                        f'max_connections=5000')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0048.py finish==')
