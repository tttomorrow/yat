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
Case Name   : 修改指定数据库，用户，会话级别的参数ssl_ciphers
Description : 1、查看ssl_ciphers默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c ssl_ciphers
              2、在gsql中分别设置数据库、用户、会话、级别ssl_ciphers；
              alter database postgres set ssl_ciphers
              to 'DHE-RSA-AES256-GCM-SHA384;
              DHE-RSA-AES128-GCM-SHA256;DHE-RSA-AES256-CCM';;
              alter user env109 set ssl_ciphers
              to 'DHE-RSA-AES256-GCM-SHA384;
              DHE-RSA-AES128-GCM-SHA256;DHE-RSA-AES256-CCM';;
              set ssl_ciphers to 'DHE-RSA-AES256-GCM-SHA384;
              DHE-RSA-AES128-GCM-SHA256;DHE-RSA-AES256-CCM';;
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
        self.log.info('==Guc_Connectionauthentication_Case0178开始==')
        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        showcmd = "source " + macro.DB_ENV_PATH \
                  + f";gsql -d {self.db_user_node.db_name} -p " \
                  + self.db_user_node.db_port + " -c \"show ssl_ciphers;\""
        self.log.info(showcmd)
        check = self.db_user_node.sh(showcmd).result()
        self.log.info(check)
        self.assertIn('ALL', check)
        self.log.info("设置ssl_ciphers，校验预期结果")
        sql_cmd = COMMONSH.execut_db_sql(
            f'''alter database postgres set ssl_ciphers 
            to 'DHE-RSA-AES256-GCM-SHA384;DHE-RSA-AES128-GCM-SHA256;
            DHE-RSA-AES256-CCM';''')
        self.log.info(sql_cmd)
        self.assertIn("ERROR", sql_cmd)
        sql_cmd1 = COMMONSH.execut_db_sql(
            f'''alter user {self.db_user_node.db_user} set ssl_ciphers 
            to 'DHE-RSA-AES256-GCM-SHA384;DHE-RSA-AES128-GCM-SHA256;
            DHE-RSA-AES256-CCM';''')
        self.log.info(sql_cmd1)
        self.assertIn("ERROR", sql_cmd1)
        sql_cmd2 = COMMONSH.execut_db_sql(
            f'''set ssl_ciphers to 'DHE-RSA-AES256-GCM-SHA384;
            DHE-RSA-AES128-GCM-SHA256;DHE-RSA-AES256-CCM';''')
        self.log.info(sql_cmd2)
        self.assertIn("ERROR", sql_cmd2)

    def tearDown(self):
        self.log.info("恢复默认值")
        gucsetcmd2 = f'''source {macro.DB_ENV_PATH};
        gs_guc set -N all -I all -c "ssl_ciphers=\'ALL\'"'''
        self.log.info(gucsetcmd2)
        self.db_user_node.sh(gucsetcmd2)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_Connectionauthentication_Case0178完成==')
