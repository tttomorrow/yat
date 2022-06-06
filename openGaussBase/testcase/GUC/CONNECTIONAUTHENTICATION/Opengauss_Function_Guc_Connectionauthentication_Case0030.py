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
Case Name   : 使用alter修改参数local_bind_address，观察预期结果；
Description : 1、查看local_bind_address默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c local_bind_address
              2、在gsql中分别设置数据库、用户、会话、级别local_bind_address；
              alter database postgres
              set local_bind_address to '100.99.81.59';
              alter user zhangyinan set local_bind_address to '100.99.81.59';
              set local_bind_address to '100.99.81.59';
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
        self.log.info('==Connectionauthentication_Case0030.py start==')
        self.rootNode = Node()
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        self.dbUserNode = Node(node='PrimaryRoot')
        self.statusCmd = f'source {macro.DB_ENV_PATH};' \
                         f'gs_om -t status --detail'

    def test_startdb(self):
        ipadd = self.dbUserNode1.db_host
        self.log.info("查询该参数默认值")
        result = COMMONSH.execute_gsguc(
            'check', ipadd, 'local_bind_address')
        self.assertTrue(result)
        self.log.info("使用alter设置local_bind_address")
        sql_cmd = COMMONSH.execut_db_sql(
            f'''alter database postgres \
            set local_bind_address to '{ipadd}';''')
        self.log.info(sql_cmd)
        self.assertIn("cannot", sql_cmd)
        sql_cmd1 = COMMONSH.execut_db_sql(
            f'''alter user {self.dbUserNode1.db_user} \
            set local_bind_address to '{ipadd}';''')
        self.log.info(sql_cmd1)
        self.assertIn("cannot", sql_cmd1)
        sql_cmd2 = COMMONSH.execut_db_sql(
            f'''set local_bind_address to '{ipadd}';''')
        self.log.info(sql_cmd2)
        self.assertIn("cannot", sql_cmd2)

    def tearDown(self):
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0030.py finish==')
