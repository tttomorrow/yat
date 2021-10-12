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
Case Name   : 使用alter修改参数port，观察预期结果；
Description : 1、查看port默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c port
              2、在gsql中分别设置数据库、用户、会话、级别port；
              alter database postgres set port to 55810;
              alter user zhangyinan set port to 55810;
              set port to 55810;
Expect      : 1、显示默认值为安装数据库时指定端口号；
              2、参数修改失败，预期结果正常；
History     :
"""

import random
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
        self.log.info('==Connectionauthentication_Case0003.py start==')
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
        self.log.info("设置随机port后使用alter设置并校验其预期结果")
        port = random.randint(1, 65535)  # 按照参数范围设置
        checkportcmd = f'lsof -i:{str(port)}'
        checkportresult = self.dbUserNode1.sh(checkportcmd).result()
        while str(port) in checkportresult:
            port = random.randint(1, 65535)
            checkportcmd = f'lsof -i:{str(port)}'
            checkportresult = self.dbUserNode1.sh(checkportcmd).result()
        sql_cmd = COMMONSH.execut_db_sql(
            f'''alter database postgres set port to '{str(port)}';''')
        self.log.info(sql_cmd)
        self.assertIn("cannot", sql_cmd)
        sql_cmd1 = COMMONSH.execut_db_sql(
            f'''alter user {self.dbUserNode1.db_user} \
            set port to '{str(port)}';''')
        self.log.info(sql_cmd1)
        self.assertIn("cannot", sql_cmd1)
        sql_cmd2 = COMMONSH.execut_db_sql(f'''set port to '{str(port)}';''')
        self.log.info(sql_cmd2)
        self.assertIn("cannot", sql_cmd2)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'port={str(self.dbUserNode1.db_port)}')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0003.py finish==')
