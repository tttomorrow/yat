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
Case Name   : port参数使用gs_guc reload设置为超边界值
Description : 1、查看port默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c port
              2、使用设置gs_guc reload设置port为超边界值
              gs_guc reload -D {cluster/dn1} -c "port=77777"
              gs_guc reload -N all  -D {cluster/dn1} -c "port=77777"
Expect      : 1、显示默认值为安装数据库时指定端口；
              2、修改失败，预期结果正常；
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
        self.log.info('==Connectionauthentication_Case0009.py start==')
        self.rootNode = Node()
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        self.dbUserNode = Node(node='PrimaryRoot')
        self.statusCmd = f'source {macro.DB_ENV_PATH};' \
                         f'gs_om -t status --detail'

    def test_startdb(self):
        self.log.info("查看port默认值，并校验；")
        result = COMMONSH.execute_gsguc('check', self.dbUserNode1.db_port,
                                       'port')
        self.assertTrue(result)
        self.log.info("使用设置gs_guc reload设置port为超边界值")
        result = COMMONSH.execute_gsguc('reload', self.constant.TPCC_ERROR,
                                        f'port=\'77777\'')
        self.assertTrue(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'port={str(self.dbUserNode1.db_port)}')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0009.py finish==')
