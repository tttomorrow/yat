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
Case Type   : GUC参数--连接认证
Case Name   : 修改参数auth_iteration_count为无效值
Description :
              1、查看auth_iteration_count默认值；
              show auth_iteration_count;
              'test'，空值、校验其预期结果；
Expect      :
              1、显示默认值为10000；
              2、参数修改失败；
"""

import unittest

from yat.test import Node

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

COMMONSH = CommonSH('PrimaryDbUser')


class GucTest(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Guc_Connectionauthentication_Case0250开始==')
        self.db_user_node = Node(node='PrimaryDbUser')

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        sql_cmd = COMMONSH.execut_db_sql('show auth_iteration_count;')
        self.log.info(sql_cmd)
        self.assertEqual('10000', sql_cmd.split('\n')[2].strip())
        self.log.info("修改auth_iteration_count为无效值")
        for i in invalid_value:
            result = COMMONSH.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"auth_iteration_count={i}")
            self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql('show auth_iteration_count;')
        self.log.info(sql_cmd)
        if '10000' != sql_cmd.split('\n')[2].strip():
            msg = COMMONSH.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'auth_iteration_count=10000')
            self.log.info(msg)
            msg = COMMONSH.restart_db_cluster()
            self.log.info(msg)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Guc_Connectionauthentication_Case0250完成==')
