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
Case Name   : 函数gs_password_deadline() 显示当前帐户密码离过期还距离多少天
Description : 查看当前帐户密码离过期还距离多少天
Expect      : 查询成功，且时间不大于90天
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Innerfunc_Security_Case0003开始-')
        self.primary_dbuser = Node('PrimaryDbUser')
        self.commonsh = CommonSH()

    def test_security_function(self):
        self.log.info('---------步骤1.查看当前帐户密码离过期还距离多少天---------')
        sql_cmd = self.commonsh.execut_db_sql(f'select '
                                              f'gs_password_deadline();')
        self.log.info(sql_cmd)
        list1 = sql_cmd.split('\n')[2]
        list2 = list1.split(' ')
        self.log.info(list2)
        str3 = list2[1]
        self.log.info(str3)
        days = int(str3)
        self.assertTrue(days <= 90)

    def tearDown(self):
        self.log.info('-----------------无需清理环境----------------')
        self.log.info('-Opengauss_Function_Innerfunc_Security_Case0003结束-')
