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
Case Name   : 使用ALTER SYSTEM SET修改数据库参数ssl_renegotiation_limit
Description : 1、查看ssl_renegotiation_limit默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c ssl_renegotiation_limit
              2、使用ALTER SYSTM SET修改数据库参数ssl_renegotiation_limit;
              ALTER SYSTEM set ssl_renegotiation_limit to 1;
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


class GucTest(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Guc_Connectionauthentication_Case0189开始==')

        self.db_user_node = Node(node='PrimaryDbUser')

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        showcmd = '''source ''' + macro.DB_ENV_PATH \
                  + ''';gs_guc check -D ''' + macro.DB_INSTANCE_PATH \
                  + ''' -c ssl_renegotiation_limit'''
        self.log.info(showcmd)
        check = self.db_user_node.sh(showcmd).result()
        self.log.info(check)
        self.assertIn('0', check)
        self.log.info("设置ssl_renegotiation_limit")
        altersql1 = "source " + macro.DB_ENV_PATH \
                    + f";gsql -d {self.db_user_node.db_name} -p " \
                    + self.db_user_node.db_port \
                    + " -c \"ALTER SYSTEM " \
                      "set ssl_renegotiation_limit to 1;\""
        res1 = self.db_user_node.sh(altersql1).result()
        self.assertIn('ERROR', res1)

    def tearDown(self):
        self.log.info("恢复默认值")
        gucsetcmd2 = f'''source {macro.DB_ENV_PATH};
        gs_guc set -N all -I all -c "ssl_renegotiation_limit=\'0\'"'''
        self.log.info(gucsetcmd2)
        self.db_user_node.sh(gucsetcmd2)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_Connectionauthentication_Case0189完成==')
