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
Case Type   : 系统管理函数
Case Name   : 备份控制函数
Description :
    1.函数pg_current_xlog_insert_location获取当前事务的插入位置
    2.函数pg_start_backup开始执行在线备份
Expect      :
    1.获取当前事务的插入位置成功
    2.函数pg_start_backup开始执行在线备份成功
History     :
"""
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0003开始执行-')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info('--步骤1.函数pg_current_xlog_insert_location获取当前事务的插入位置--')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_current_xlog_insert_location();')
        LOG.info(sql_cmd)
        self.assertIn('1 row', sql_cmd)
        LOG.info('---------步骤2.函数pg_start_backup开始执行在线备份---------')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_start_backup(\'label_goes_here\');')
        LOG.info(sql_cmd)
        self.assertIn('1 row', sql_cmd)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0003结束-')
