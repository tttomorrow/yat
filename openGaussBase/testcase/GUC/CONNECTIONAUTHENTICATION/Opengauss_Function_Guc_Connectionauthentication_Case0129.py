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
Case Name   : 修改指定数据库，用户，会话级别的参数authentication_timeout
Description :
              1、查看authentication_timeout默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c authentication_timeout
              2、在gsql中分别设置数据库、用户、会话、级别authentication_timeout
              alter database postgres set authentication_timeout to '10min';
              alter user env109 set authentication_timeout to '10min';
              set authentication_timeout to '10min';
Expect      : 
              1、显示默认值；
              2、参数修改失败；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

COMMONSH = CommonSH('PrimaryDbUser')


class GucTest(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Guc_Connectionauthentication_Case0129开始==')

        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        sql_cmd = COMMONSH.execut_db_sql('''show authentication_timeout;''')
        self.log.info(sql_cmd)
        self.assertEqual("1min", sql_cmd.split("\n")[-2].strip())

        self.log.info("设置authentication_timeout，校验预期结果")
        sql_cmd = COMMONSH.execut_db_sql(
            f'''alter database postgres set authentication_timeout \
            to '10min';''')
        self.log.info(sql_cmd)
        self.assertIn("ERROR", sql_cmd)
        sql_cmd1 = COMMONSH.execut_db_sql(
            f'''alter user {self.db_user_node.db_user} \
            set authentication_timeout to '10min';''')
        self.log.info(sql_cmd1)
        self.assertIn("ERROR", sql_cmd1)
        sql_cmd2 = COMMONSH.execut_db_sql(
            f'''set authentication_timeout to '10min';''')
        self.log.info(sql_cmd2)
        self.assertIn("ERROR", sql_cmd2)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                        f"authentication_timeout=1min")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info("查询该参数默认值")
        sql_cmd = COMMONSH.execut_db_sql('''show authentication_timeout;''')
        self.log.info(sql_cmd)
        self.assertEqual("1min", sql_cmd.split("\n")[-2].strip())
        self.log.info('==Guc_Connectionauthentication_Case0129完成==')
