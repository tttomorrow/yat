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
Case Type   : 函数和操作符-安全函数
Case Name   : 查看登录用户的登录信息
Description :
    1.查看上一次登录认证通过的日期、时间和IP等信息
Expect      :
    1.正确显示上一次登录认证通过的日期、时间和IP等信息
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Innerfunc_Security_Case0009开始-')
        self.primary_dbuser = Node('PrimaryDbUser')
        self.commonsh = CommonSH()

    def test_security_function(self):
        self.log.info('---步骤1.查看上一次登录认证通过的日期、时间和IP等信息--')
        sql_cmd = self.commonsh.execut_db_sql(f'select * from login_audit'
                                              f'_messages_pid(true);')
        self.log.info(sql_cmd)
        self.assertIn('login_success', sql_cmd)

    def tearDown(self):
        self.log.info('-----------------无需清理环境----------------')
        self.log.info('-Opengauss_Function_Innerfunc_Security_Case0009结束-')
