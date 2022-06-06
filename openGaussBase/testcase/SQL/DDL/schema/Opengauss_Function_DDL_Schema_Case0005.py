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
Case Type   : 基础功能
Case Name   : 修改模式用户
Description :
    1.创建用户
    2.使用系统用户修改
    3.修改用户不是所有者 ，不是新用户member，没有createdb权限
    4.修改用户不是所有者 ，不是新用户member，有createdb权限
    5.修改用户不是所有者 ，是新用户直接member，无createdb权限
    6.修改用户不是所有者 ，是新用户间接member，无createdb权限
    7.修改用户是所有者 ，不是新用户member，无createdb权限
    8.修改用户是所有者 ，是新用户直接member，无createdb权限
    9.修改用户是所有者 ，是新用户间接member，无createdb权限
    10.修改用户是所有者 ，是新用户直接member，有createdb权限
    11.修改用户是所有者 ，是新用户间接member，有createdb权限
    12.修改用户不是所有者 ，是新用户直接member，有createdb权限
    13.修改用户不是所有者 ，是新用户间接member，有createdb权限
    14.修改用户是所有者 ，不是新用户member，有createdb权限
Expect      :
    1.创建用户成功
    2.创建成功
    3.修改失败
    4.修改失败
    5.修改失败
    6.修改失败
    7.修改失败
    8.修改失败
    9.修改失败
    10.修改成功
    11.修改成功
    12.修改失败
    13.修改失败
    14.修改失败
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Ddlschema(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Schema_Case0005.py start--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.username = 'user_case005'
        self.groupname = 'group_case005'
        self.password = macro.COMMON_PASSWD

    def test_schema(self):
        self.log.info('----------------1.创建用户-----------------')
        sql = f"create user {self.username} " \
              f"with password '{self.password}';" \
              f"create user {self.username}_1 " \
              f"with password '{self.password}';" \
              f"create user {self.groupname} " \
              f"with password '{self.password}';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)
        sql = f"create user {self.groupname}_1 " \
              f"with password '{self.password}' IN GROUP {self.groupname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)
        sql = f"create user {self.groupname}_2 " \
              f"with password '{self.password}' IN GROUP {self.groupname}_1;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)

        self.log.info('----------2.使用系统用户修改----------')
        sql = f"alter schema {self.username}_1  owner to {self.username};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---3.修改用户不是所有者 ，不是新用户member，没有createdb权限---')
        sql = f"alter schema {self.username} owner to {self.groupname};"
        cmd = f"-U {self.username}_1 -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertNotIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---4.修改用户不是所有者 ，不是新用户member，有createdb权限---')
        sql = f"grant create on database  " \
              f"{self.db_primary_db_user.db_name} to {self.username}_1;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, result)
        sql = f"alter schema {self.username} owner to {self.groupname};"
        cmd = f"-U {self.username}_1 -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertNotIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---5.修改用户不是所有者 ，是新用户直接member，无createdb权限---')
        sql = f"alter schema {self.username} owner to {self.groupname};"
        cmd = f"-U {self.groupname}_1 -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertNotIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---6.修改用户不是所有者 ，是新用户间接member，无createdb权限---')
        sql = f"alter schema {self.username} owner to {self.groupname};"
        cmd = f"-U {self.groupname}_2 -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertNotIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---7.修改用户是所有者 ，不是新用户member，无createdb权限---')
        sql = f"alter schema {self.username} owner to {self.groupname};"
        cmd = f"-U {self.username} -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertNotIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---8.修改用户是所有者 ，是新用户直接member，无createdb权限---')
        sql = f"alter schema {self.groupname}_1 owner to {self.groupname};"
        cmd = f"-U {self.groupname}_1 -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertNotIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---9.修改用户是所有者 ，是新用户间接member，无createdb权限---')
        sql = f"alter schema {self.groupname}_2 owner to {self.groupname};"
        cmd = f"-U {self.groupname}_2 -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertNotIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---10.修改用户是所有者 ，是新用户直接member，有createdb权限---')
        sql = f"grant create on database  {self.db_primary_db_user.db_name}" \
              f" to {self.groupname}_1;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, result)
        sql = f"alter schema {self.groupname}_1 owner to {self.groupname};"
        cmd = f"-U {self.groupname}_1 -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---11.修改用户是所有者 ，是新用户间接member，有createdb权限---')
        sql = f"grant create on database  {self.db_primary_db_user.db_name}" \
              f" to {self.groupname}_2;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, result)
        sql = f"alter schema {self.groupname}_2 owner to {self.groupname};"
        cmd = f"-U {self.groupname}_2 -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---12.修改用户不是所有者 ，是新用户直接member，有createdb权限---')
        sql = f"grant create on database  {self.db_primary_db_user.db_name}" \
              f" to {self.groupname}_1;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, result)
        sql = f"alter schema {self.username} owner to {self.groupname};"
        cmd = f"-U {self.groupname}_1 -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertNotIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---13.修改用户不是所有者 ，是新用户间接member，有createdb权限---')
        sql = f"grant create on database  {self.db_primary_db_user.db_name}" \
              f" to {self.groupname}_2;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, result)
        sql = f"alter schema {self.username} owner to {self.groupname};"
        cmd = f"-U {self.groupname}_2 -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertNotIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('---14.修改用户是所有者 ，不是新用户member，有createdb权限---')
        sql = f"grant create on database  {self.db_primary_db_user.db_name}" \
              f" to {self.username};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, result)
        sql = f"alter schema {self.username} owner to {self.groupname};"
        cmd = f"-U {self.username} -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertNotIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

    def tearDown(self):
        self.log.info('------------环境清理-----------')
        self.log.info('---------删除用户------')
        sql = f"drop user if exists {self.username} cascade;" \
              f"drop user if exists {self.username}_1 cascade;" \
              f"drop user if exists {self.groupname} cascade;" \
              f"drop user if exists {self.groupname}_1 cascade;" \
              f"drop user if exists {self.groupname}_2 cascade;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('--Opengauss_Function_DDL_Schema_Case0005.py finish-')
