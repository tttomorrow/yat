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
Case Name   : 修改参数tcp_keepalives_idle,观察预期结果，通过Unix域套接字做
              的链接忽略这个参数
Description : 1、查看tcp_keepalives_idle默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c tcp_keepalives_idle
              2、使用设置gs_guc set设置tcp_keepalives_idle
              gs_guc set -D {cluster/dn1} -c "tcp_keepalives_idle=120"
              3、校验是否修改成功；
              show tcp_keepalives_idle;
              4、恢复默认值
Expect      : 1、显示默认值；
              2、参数修改成功；
              3、查看参数修改成功；
              4、修改成功；
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
        self.log.info('==Guc_Connectionauthentication_Case0229开始==')

        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        showcmd = "source " + macro.DB_ENV_PATH \
                  + f";gsql -d {self.db_user_node.db_name} -p " \
                  + self.db_user_node.db_port \
                  + " -c \"show tcp_keepalives_idle;\""
        self.log.info(showcmd)
        check = self.db_user_node.sh(showcmd).result()
        self.log.info(check)
        self.assertIn('1min', check)
        self.log.info("设置tcp_keepalives_idle，重启使其生效")
        gucsetcmd2 = '''source ''' + macro.DB_ENV_PATH \
                     + ''';gs_guc set -D ''' + macro.DB_INSTANCE_PATH \
                     + ''' -c "tcp_keepalives_idle=120"'''
        self.log.info(gucsetcmd2)
        self.db_user_node.sh(gucsetcmd2)
        COMMONSH.restart_db_cluster()
        self.log.info("校验参数是否修改成功")
        connectcmd = '''source ''' + macro.DB_ENV_PATH \
                     + ''';gs_guc check -D ''' + macro.DB_INSTANCE_PATH \
                     + ''' -c "tcp_keepalives_idle"'''
        self.log.info(connectcmd)
        res1 = self.db_user_node.sh(connectcmd).result()
        self.log.info(res1)
        self.assertIn('120', res1)

    def tearDown(self):
        self.log.info("恢复默认值")
        gucsetcmd2 = f'''source {macro.DB_ENV_PATH};
        gs_guc set -N all -I all -c "tcp_keepalives_idle=\'1min\'"'''
        self.log.info(gucsetcmd2)
        self.db_user_node.sh(gucsetcmd2)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_Connectionauthentication_Case0229完成==')
