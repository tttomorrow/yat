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
Case Name   : auth_iteration_count参数使用gs_guc reload设置为空值
Description : 1、查看auth_iteration_count默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c auth_iteration_count
              2、使用设置gs_guc reload设置auth_iteration_count为空值
              gs_guc reload -D {cluster/dn1} -c "auth_iteration_count=' '"
Expect      : 1、显示默认值；
              2、参数修改失败；
"""

import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

COMMONSH = CommonSH('PrimaryDbUser')


class GucTest(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Guc_Connectionauthentication_Case0148开始==')
        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        sql_cmd = COMMONSH.execut_db_sql('show auth_iteration_count;')
        self.log.info(sql_cmd)
        self.assertEqual('10000', sql_cmd.split('\n')[2].strip())
        self.log.info("设置auth_iteration_count为空值")
        set_cmd = '''source ''' + macro.DB_ENV_PATH \
                     + ''';gs_guc reload -D ''' + macro.DB_INSTANCE_PATH \
                     + ''' -c "auth_iteration_count=\' \'"'''
        self.log.info(set_cmd)
        msg = self.db_user_node.sh(set_cmd).result()
        self.log.info(msg)
        self.assertIn('ERROR', msg)

    def tearDown(self):
        self.log.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql('show auth_iteration_count;')
        if '10000' != sql_cmd.split('\n')[2].strip():
            msg = COMMONSH.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f'auth_iteration_count=10000')
            self.log.info(msg)
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_Connectionauthentication_Case0148完成==')
