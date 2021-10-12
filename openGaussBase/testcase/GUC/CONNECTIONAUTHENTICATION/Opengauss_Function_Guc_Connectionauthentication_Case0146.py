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
Case Name   : 使用ALTER SYSTEM SET修改参数auth_iteration_count为其他数据类型
Description : 1、查看auth_iteration_count默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c auth_iteration_count
              2、使用ALTER SYSTM SET修改参数auth_iteration_count为其他数据类型;
              ALTER SYSTEM set auth_iteration_count to 'test';
Expect      : 1、显示默认值；
              2、参数修改失败；
History     :
"""

import unittest


from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

COMMONSH = CommonSH('PrimaryDbUser')


class GucTest(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Guc_Connectionauthentication_Case0146开始==')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        result = COMMONSH.execute_gsguc(
            'check', '10000', 'auth_iteration_count')
        self.assertTrue(result)

        self.log.info("设置auth_iteration_count为其他数据类型")
        sql_cmd = COMMONSH.execut_db_sql(
            f'''ALTER SYSTEM set auth_iteration_count to 'test';''')
        self.log.info(sql_cmd)
        self.assertIn("ERROR", sql_cmd)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                        f'auth_iteration_count=10000')
        self.log.info(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_Connectionauthentication_Case0146完成==')
