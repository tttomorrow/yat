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
Case Name   : 修改指定数据库，用户，会话级别的参数auth_iteration_count
Description : 1、查看auth_iteration_count默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c auth_iteration_count
              2、在gsql中分别设置数据库、用户、会话、级别auth_iteration_count；
              alter database postgres set auth_iteration_count to 11111;
              alter user env109 set auth_iteration_count to 11111;
              set auth_iteration_count to 11111;
Expect      : 1、显示默认值；
              2、参数修改失败；
History     :
"""


import unittest



from yat.test import Node
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

COMMONSH = CommonSH('PrimaryDbUser')


class GucTest(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Guc_Connectionauthentication_Case0142开始==')
        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        result = COMMONSH.execute_gsguc(
            'check', '10000', 'auth_iteration_count')
        self.assertTrue(result)

        self.log.info("设置auth_iteration_count，校验预期结果")
        sql_cmd = COMMONSH.execut_db_sql(
            f'''alter database postgres 
            set auth_iteration_count to 11111;''')
        self.log.info(sql_cmd)
        self.assertIn("ERROR", sql_cmd)

        sql_cmd1 = COMMONSH.execut_db_sql(
            f'''alter user {self.db_user_node.db_user} 
            set auth_iteration_count to 11111;''')
        self.log.info(sql_cmd1)
        self.assertIn("ERROR", sql_cmd1)

        sql_cmd2 = COMMONSH.execut_db_sql(
            f'''set auth_iteration_count to 11111;''')
        self.log.info(sql_cmd2)
        self.assertIn("ERROR", sql_cmd2)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                        f'auth_iteration_count=10000')
        self.log.info(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_Connectionauthentication_Case0142完成==')
