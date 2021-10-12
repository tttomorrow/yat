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
Case Type   : 功能测试
Case Name   : 创建用户赋予管理员权限再收回管理员权限，修改3种类型参数:合理报错
Description :
    1.创建用户赋予管理员权限再收回管理员权限创建用户 期望:创建成功
    2.修改postmaster类型 期望:修改失败，报错无权限，参数未被修改
    3.修改bankend类型 期望:修改失败，报错无权限，参数未被修改
    4.修改sighup类型 期望:修改失败，报错无权限，参数未被修改
    5.清理环境
Expect      :
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro

LOGGER = Logger()


class Altertestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info('==Opengauss_Function_Alter_System_Set_Case0002开始执行==')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_alter(self):
        LOGGER.info('==创建用户 期望:创建成功==')
        sql_cmd = self.commonsh.execut_db_sql(f'''drop schema \
            if exists system_user_002 cascade;\
            DROP USER IF EXISTS system_user_002;\
            CREATE USER system_user_002 PASSWORD '{macro.COMMON_PASSWD}';\
            grant all privileges to system_user_002;\
            REVOKE all privileges FROM system_user_002;\
            ''')
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)

        LOGGER.info('==修改postmaster类型 期望:修改失败，报错无权限，参数未被修改==')
        sql_cmd = self.commonsh.execut_db_sql(f'''SET SESSION AUTHORIZATION \
            system_user_002 PASSWORD '{macro.COMMON_PASSWD}';\
            show audit_directory;\
            ALTER SYSTEM SET audit_directory to pg_clog;\
            show audit_directory;\
            ''')
        LOGGER.info(sql_cmd)
        self.assertIn("SET", sql_cmd)
        self.assertIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertIn("must be superuser to examine", sql_cmd)
        self.assertIn("must be sysadmin to execute", sql_cmd)

        LOGGER.info('==修改bankend类型 期望:修改失败，报错无权限，参数未被修改==')
        sql_cmd = self.commonsh.execut_db_sql(f'''SET SESSION AUTHORIZATION \
            system_user_002 PASSWORD '{macro.COMMON_PASSWD}';\
            show log_disconnections;\
            ALTER SYSTEM SET log_disconnections to on;\
            show log_disconnections;\
            ''')
        LOGGER.info(sql_cmd)
        self.assertIn("SET", sql_cmd)
        self.assertIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertIn("must be sysadmin to execute", sql_cmd)

        LOGGER.info('==修改sighup类型 期望:修改失败，报错无权限，参数未被修改==')
        sql_cmd = self.commonsh.execut_db_sql(f'''SET SESSION AUTHORIZATION \
            system_user_002 PASSWORD '{macro.COMMON_PASSWD}';\
            show archive_command;\
            ALTER SYSTEM SET archive_command to 'cp %p /usr/%f';\
            show archive_command;\
            ''')
        LOGGER.info(sql_cmd)
        self.assertIn("SET", sql_cmd)
        self.assertIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertIn("must be sysadmin to execute", sql_cmd)

    def tearDown(self):
        LOGGER.info('==-this is teardown==--')
        sql_cmd = self.commonsh.execut_db_sql(f"DROP USER system_user_002")
        LOGGER.info(sql_cmd)
        LOGGER.info('==Opengauss_Function_Alter_System_Set_Case0002执行结束==--')
