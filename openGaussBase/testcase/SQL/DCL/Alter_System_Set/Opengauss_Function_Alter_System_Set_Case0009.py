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
Case Type   : SQL_DCL
Case Name   : audit_set_parameter有管理员权限：审计set
Description :
    1.查看audit_set_parameter默认值，期望默认值为1
    2.修改audit_set_parameter默认值为0
    3.恢复环境，改回默认值再进行审计
    4.恢复环境默认值
Expect      :
    1.查看audit_set_parameter默认值，期望默认值为1
    2.修改audit_set_parameter默认值为0
    3.恢复环境，改回默认值再进行审计成功
    4.恢复环境默认值成功
History     : 
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import Node


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_Alter_System_Set_Case0009开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_built_in_func(self):
        self.log.info('-----步骤1.查看audit_set_parameter默认值，期望默认值为1-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f"show audit_set_parameter;")
        self.log.info(sql_cmd)
        self.assertIn('1', sql_cmd)

        self.log.info('-----步骤2.修改audit_set_parameter默认值为0-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f"ALTER SYSTEM SET audit_set_parameter to 0;"
            f"select count(*) FROM pg_query_audit"
            f"('2000-01-01 08:00:00','9999-01-01 08:00:00');"
            f"ALTER SYSTEM SET audit_set_parameter to 0;"
            f"show audit_set_parameter;"
            f"select count(*) FROM pg_query_audit"
            f"('2000-01-01 08:00:00','9999-01-01 08:00:00');")
        self.log.info(sql_cmd)
        str_info1 = sql_cmd.split('\n')[-2]
        self.log.info(f'str_info1 = {str_info1}')

        self.log.info('-----步骤3.恢复环境，改回默认值再进行审计-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f"ALTER SYSTEM SET audit_set_parameter to 1;"
            f"show audit_set_parameter;"
            f"set log_planner_stats = off;"
            f"select count(*) FROM pg_query_audit"
            f"('2000-01-01 08:00:00','9999-01-01 08:00:00');")
        self.log.info(sql_cmd)
        str_info2 = sql_cmd.split('\n')[-2]
        self.log.info(f'str_info2 = {str_info2}')
        self.assertTrue(int(str_info2) > int(str_info1))

    def tearDown(self):
        self.log.info('-----步骤4.恢复环境默认值-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f"ALTER SYSTEM SET audit_set_parameter to 1;")
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_Alter_System_Set_Case0009结束')
