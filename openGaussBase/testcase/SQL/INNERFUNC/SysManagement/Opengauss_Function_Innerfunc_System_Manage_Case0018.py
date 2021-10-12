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
Case Type   : 系统管理函数-恢复控制函数
Case Name   : 函数pg_is_in_recovery() ，查看备机状态，如果恢复仍然在进行中则返回true
Description :
    1.备机执行函数pg_is_in_recovery()
    2.主机执行函数pg_is_in_recovery()
Expect      :
    1.备机执行函数pg_is_in_recovery()，返回true
    2.主机执行函数pg_is_in_recovery()，返回false
History     : 
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(), '单机环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0018开始-')
        self.commonsh = CommonSH('Standby1DbUser')
        self.commonsh1 = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info(f'---步骤1.备机执行函数pg_is_in_recovery()，返回true---')
        sql_cmd = self.commonsh.execut_db_sql(f'select pg_is_in_recovery();')
        LOG.info(sql_cmd)
        self.assertIn('t', sql_cmd)

        LOG.info(f'---步骤2.主机执行函数pg_is_in_recovery()，执行返回false---')
        sql_cmd = self.commonsh1.execut_db_sql(f'select pg_is_in_recovery();')
        LOG.info(sql_cmd)
        self.assertIn('f', sql_cmd)

    def tearDown(self):
        LOG.info('-----无需清理环境------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0018结束-')
