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
Case Type   : 系统信息函数
Case Name   : 函数pg_control_checkpoint()，返回系统控制文件状态
Description :
    1.函数pg_control_checkpoint()，返回系统控制文件状态
Expect      :
    2.返回系统控制文件状态成功
History     : 
"""

import unittest
import time
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Functions(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Innerfunc_Transactions_Id_Case0001开始-')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        date1 = time.strftime("%Y-%m-%d", time.localtime())
        self.log.info(date1)
        self.log.info(f'-步骤1.函数pg_control_checkpoint()，返回系统控制文件状态-')
        sql_cmd = self.commonsh.execut_db_sql(f'select pg_control_system();')
        self.log.info(sql_cmd)
        self.assertIn(f'{date1}', sql_cmd)

    def tearDown(self):
        self.log.info('-------无需清理环境-------')
        self.log.info(
            '-Opengauss_Function_Innerfunc_Transactions_Id_Case0001结束-')
