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
Case Name   : ssl_ciphers参数使用gs_guc set设置为空值
Description : 1、查看ssl_ciphers默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c ssl_ciphers
              2、使用设置gs_guc set设置ssl_ciphers为空值，重启使其生效;
              gs_guc set -D {cluster/dn1} -c "ssl_ciphers=' '"
              gs_guc set -N all  -D {cluster/dn1} -c "ssl_ciphers=' '"
Expect      : 1、显示默认值；
              2、参数修改成功，重启失败；
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
        self.log.info('==Guc_Connectionauthentication_Case0183开始==')

        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        showcmd = "source " + macro.DB_ENV_PATH \
                  + f";gsql -d {self.db_user_node.db_name} -p "\
                  + self.db_user_node.db_port + " -c \"show ssl_ciphers;\""
        self.log.info(showcmd)
        check = self.db_user_node.sh(showcmd).result()
        self.log.info(check)
        self.assertIn('ALL', check)
        self.log.info("设置ssl_ciphers为空值，重启使其生效")
        gucsetcmd2 = '''source ''' + macro.DB_ENV_PATH \
                     + ''';gs_guc set -D ''' + macro.DB_INSTANCE_PATH \
                     + ''' -c "ssl_ciphers=\' \'"'''
        self.log.info(gucsetcmd2)
        res1 = self.db_user_node.sh(gucsetcmd2).result()
        self.log.info(res1)
        self.assertIn('Success to perform gs_guc', res1)
        self.log.info("重启使其生效，观察预期结果")
        result = COMMONSH.restart_db_cluster()
        self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        gucsetcmd2 = f'''source {macro.DB_ENV_PATH};
        gs_guc set -N all -I all -c "ssl_ciphers=\'ALL\'"'''
        self.log.info(gucsetcmd2)
        self.db_user_node.sh(gucsetcmd2)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_Connectionauthentication_Case0183完成==')
