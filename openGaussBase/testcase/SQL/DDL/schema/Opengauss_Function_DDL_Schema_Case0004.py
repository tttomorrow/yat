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
Case Type   : 基础功能
Case Name   : 修改模式名称
Description :
    1.创建模式
    2.使用系统用户修改名称
    3.修改一个不存在的schema
    4.创建用户
    5.使用test_user修改数据库
    6.给用户赋予权限
    7.使用test_user修改数据库
    8.删除用户test_user，在重新创建用户
    9.修改schema名称
Expect      :
    1.创建成功
    2.修改成功
    3.修改失败，提示not exist
    4.创建成功
    5.修改失败，提示permission denied
    6.赋权成功
    7.修改成功
    8.删除成功，并且重新创建用户成功
    9.修改成功
History     :
"""

import unittest
import time
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DdlDatabase(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Schema_Case0004.py start--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.schname = 'schema_case003'
        self.username = 'user_case003'
        self.password = 'test@12345'

    def test_basebackup(self):
        self.log.info('------1.创建模式-------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname} "
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------2.使用系统用户修改名称----')
        sql = f"alter schema {self.schname} rename to {self.schname}_new;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('--------3.修改一个不存在的schema----------------')
        sql = f"alter schema not_exist rename to schema_1;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.NOT_EXIST, result)

        self.log.info('--------4.创建用户----------------')
        sql = f"create user {self.username} with password '{self.password}';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)

        self.log.info('------5.使用test_user修改数据库-------')
        sql = f"alter schema {self.schname}_new rename to {self.schname};"
        cmd = f"-U {self.username} -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.PERMISSION_DENIED, result)

        self.log.info('------6.给用户赋予权限-------')
        sql = f"grant all on database" \
            f" {self.db_primary_db_user.db_name} to {self.username};" \
            f"grant alter on schema {self.schname}_new to {self.username};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, result)

        self.log.info('------7.使用test_user修改数据库-------')
        sql = f"alter schema {self.schname}_new rename to {self.schname};"
        cmd = f"-U {self.username} -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------8.删除用户test_user，再重新创建用户-------')
        sql = f"drop user {self.username} cascade;" \
            f"create user {self.username} with password '{self.password}';" \
            f"grant create on database " \
            f"{self.db_primary_db_user.db_name} to {self.username};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)

        self.log.info('------9.修改schema名称-------')
        sql = f"alter schema {self.username} rename to {self.username}_new;"
        cmd = f"-U {self.username} -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)

    def tearDown(self):
        self.log.info('------------环境清理-----------')
        self.log.info('---------删除schema------')
        result = self.commonshpri.execut_db_sql(
            f"drop schema if exists {self.schname};")
        self.log.info(result)
        result = self.commonshpri.execut_db_sql(
            f"drop schema if exists {self.username};")
        self.log.info(result)
        result = self.commonshpri.execut_db_sql(
            f"drop schema if exists {self.schname}_new ;")
        self.log.info(result)
        result = self.commonshpri.execut_db_sql(
            f"drop schema if exists {self.username}_new;")
        self.log.info(result)

        self.log.info('---------删除用户------')
        result = self.commonshpri.execut_db_sql(
            f"drop user if exists {self.username} cascade;")
        self.log.info(result)

        self.log.info('--Opengauss_Function_DDL_Schema_Case0004.py finish-')
