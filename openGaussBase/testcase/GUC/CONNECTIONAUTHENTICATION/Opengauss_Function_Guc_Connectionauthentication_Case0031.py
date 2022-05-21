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
Case Name   : 使用ALTER SYSTEM SET修改参数local_bind_address，观察预期结果；
Description : 1、查看local_bind_address默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c local_bind_address
              2、使用ALTER SYSTEM SET修改数据库参数local_bind_address;
              ALTER SYSTEM SET  local_bind_address to '100.99.81.59';
              3、重启使其生效；
              gs_om -t stop && gs_om -t start
              4、恢复默认值
Expect      : 1、显示默认值；
              2、参数修改成功；
              3、重启成功；
              4、恢复默认值；
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
        self.log.info('==Connectionauthentication_Case0031.py start==')
        self.rootNode = Node()
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        self.dbUserNode = Node(node='PrimaryRoot')
        self.statusCmd = f'source {macro.DB_ENV_PATH};' \
                         f'gs_om -t status --detail'

    def test_startdb(self):
        self.ipadd = self.dbUserNode1.db_host
        self.log.info("查询该参数默认值")
        result = COMMONSH.execute_gsguc('check', self.ipadd,
                                       'local_bind_address')
        self.assertTrue(result)
        self.log.info("使用aLTER SYSTEM SET设置local_bind_address")
        sql_cmd = COMMONSH.execut_db_sql(
            f'''ALTER SYSTEM set \
            local_bind_address to \'{self.ipadd}\';''')
        self.log.info(sql_cmd)
        self.assertIn("ALTER SYSTEM SET", sql_cmd)
        self.log.info("重启使其生效，观察预期结果")
        COMMONSH.restart_db_cluster()

    def tearDown(self):
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'local_bind_address=\'{self.ipadd}\'',
            single=True)
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0031.py finish==')
