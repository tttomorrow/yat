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
Case Type   : 系统管理函数-其他函数
Case Name   : 使用函数pg_get_flush_lsn(),返回当前节点flush的xlog位置
Description : 使用函数pg_get_flush_lsn(),返回当前节点flush的xlog位置
Expect      : 使用函数pg_get_flush_lsn(),返回当前节点flush的xlog位置成功
History     : 
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0014开始-')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info(f'--步骤1.使用函数pg_get_flush_lsn(),返回当前节点flush的xlog位置--')
        sql_cmd = self.commonsh.execut_db_sql(f'select '
                                              f'pg_get_flush_lsn();')
        LOG.info(sql_cmd)
        self.assertIn('1 row', sql_cmd)
        list1 = sql_cmd.split('\n')[2]
        list2 = list1.split('/')
        LOG.info(len(list2))
        self.assertEqual(len(list2), 2)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0014结束-')
