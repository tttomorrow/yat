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
Case Name   : local_bind_address参数使用gs_guc set设置
Description : 1、查看local_bind_address默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c local_bind_address
              2、使用设置gs_guc set设置local_bind_address
              gs_guc set -D {cluster/dn1}
              -c "local_bind_address='100.99.81.59'"
              3、在相应配置文件中查看校验配置，重启使其生效；
              cat {cluster/dn1}/postgresql.conf | grep local_bind_address
              gs_om -t stop && gs_om -t start
              4、恢复默认值
Expect      : 1、显示默认值；
              2、参数修改成功；
              3、查看参数修改成功，重启成功；
              4、修改成功；
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
        self.log.info('==Connectionauthentication_Case0028.py start==')
        self.rootNode = Node()
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        self.dbUserNode = Node(node='PrimaryRoot')
        self.statusCmd = f'source {macro.DB_ENV_PATH};' \
                         f'gs_om -t status --detail'

    def test_startdb(self):
        ipadd = self.dbUserNode1.db_host
        self.log.info("查询该参数默认值")
        result = COMMONSH.execute_gsguc('check', ipadd, 'local_bind_address')
        self.assertTrue(result)
        self.log.info("使用设置gs_guc set设置local_bind_address")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                        f'local_bind_address=\'{ipadd}\'',
                                        single=True)
        self.assertTrue(result)
        self.log.info("在相应配置文件中查看校验配置")
        catcmd = f'''cat {macro.DB_INSTANCE_PATH}/postgresql.conf | \
        grep local_bind_address'''
        catresult = self.dbUserNode1.sh(catcmd).result()
        self.assertIn(ipadd, catresult)
        self.log.info("重启数据库使其生效,预期成功")
        COMMONSH.restart_db_cluster()

    def tearDown(self):
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0028.py finish==')
