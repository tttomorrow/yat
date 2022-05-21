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
Case Name   : 使用管理员用户和普通用户修改数据库名称和用户
Description :
    1.创建普通用户A和B
    2.使用用户test创建数据库
    3.使用管理员用户修改数据库所有者
    4.使用用户B修改数据库名称
    5.使用用户A修改数据库名称
    6.使用原数据库名插入数据
    7.使用新数据库名插入数据
Expect      :
    1.创建用户成功
    2.创建数据库成功
    3.修改所有者成功
    4.修改名称失败，提示无权限
    5.修改失败，提示无权限
    6.创建表失败，提示无权限
    7.创建表并插入数据成功
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DdlDatabaseCase0006(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Database_Case0006.py 开始执行--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.db_primary_root_node = Node(node='PrimaryRoot')
        self.constant = Constant()
        self.dbname = 'database_case011'
        self.dbname_new = 'database_case011_new'
        self.tblname = 'tbl_case011'
        self.username = 'user_case011'
        self.username_new = 'user_case011_new'
        self.username_without = 'user_case011_without'
        self.password = 'test@2345234'

    def test_database_case0006(self):
        self.log.info('---1.创建普通用户A和B:成功---------')
        sql = f"create user {self.username} CREATEDB " \
            f" password '{self.password}';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)
        result = self.commonshpri.execut_db_sql(
            f"create user {self.username_new} CREATEDB "
            f"password '{self.password}';")
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)
        sql = f"create user {self.username_without} CREATEDB  \
        password '{self.password}' IN ROLE {self.username_new};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)

        self.log.info('---2.使用用户test创建数据库:成功')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists {self.dbname};"
            f"create database {self.dbname};")
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('-3.使用数据库非所有者修改数据库所有者:失败-----------')
        sql = f"ALTER DATABASE {self.dbname}  OWNER TO  {self.username};"
        cmd = f'-U {self.username} -W {self.password}'
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(f"must be owner of database {self.dbname}", result)

        self.log.info('-4.使用管理员用户修改数据库所有者:成功-----------')
        sql = f"ALTER DATABASE {self.dbname}  OWNER TO  {self.username};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('5.使用数据库所有者修改数据库所有者非新用户成员:失败--------')
        sql = f"ALTER DATABASE {self.dbname}  OWNER TO  {self.username_new};"
        cmd = f'-U {self.username} -W {self.password}'
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        expect = f'must be member of role "{self.dbname_new}"'
        self.assertNotIn(expect, result)

        self.log.info('-----------6.使用管理员用户修改数据库所有者:成功----------')
        sql = f"ALTER DATABASE {self.dbname} " \
            f" OWNER TO  {self.username_without};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('7.使用据库所有者且为新用户成员修改数据库所有者成功---------')
        sql = f"ALTER DATABASE {self.dbname}  OWNER TO  {self.username_new};"
        cmd = f'-U {self.username_without} -W {self.password}'
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('-8.使用管理员用户修改数据库名称:成功-----')
        sql = f"ALTER DATABASE {self.dbname}  rename TO  {self.dbname_new};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('----------9.使用原数据库名插入数据--------')
        sql = f"create table {self.tblname}(i int);"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn(f'database "{self.dbname}" does not exist', result)

        self.log.info('----------10.使用新数据库名插入数据--------')
        sql = f"create table {self.tblname}(i int);" \
            f"insert into {self.tblname} values(1);"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname_new)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)

        self.log.info('-------11.使用用户user_new修改数据库名称:成功-----')
        sql = f"ALTER DATABASE {self.dbname_new}  rename TO  {self.dbname};"
        cmd = f'-U {self.username_new} -W {self.password}'
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('-------12.使用数据库所有者且有CREATEDB权限用户修改数据库名称:成功-------')
        sql = f"ALTER DATABASE {self.dbname}  rename TO  {self.dbname_new};"
        cmd = f'-U {self.username_new} -W {self.password}'
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('--------13.使用数据库所有者且无CREATEDB权限用户修改数据库名称:失败---------')
        sql = f'alter user {self.username_new} NOCREATEDB;'
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, result)
        sql = f'alter database {self.dbname_new} rename to {self.dbname};'
        cmd = f'-U {self.username_new} -W {self.password}'
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.PERMISSION_DENIED, result)

        self.log.info('--------12.使用非数据库所有者且有CREATEDB权限用户修改数据库名称:成功--------')
        sql = f"ALTER DATABASE {self.dbname_new}  rename TO  {self.dbname};"
        cmd = f'-U {self.username} -W {self.password}'
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.PERMISSION_DENIED, result)

    def tearDown(self):
        self.log.info('-环境清理')
        self.log.info('----------删除数据库--------')
        sql = f"drop database if exists {self.dbname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        sql = f"drop database if exists {self.dbname_new};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('----------删除用户--------')
        sql = f"drop user if exists {self.username};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        sql = f"drop user if exists {self.username_new};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        sql = f"drop user if exists {self.username_without};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('---Opengauss_Function_DDL_Database_Case0006.py 执行结束--')
