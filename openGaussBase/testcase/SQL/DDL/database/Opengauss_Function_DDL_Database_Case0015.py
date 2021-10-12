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
Case Name   : 不同权限用户删除数据库
Description :
    1.创建数据库
    2.连接该数据库，使用系统用户删除数据库
    3.创建用户并赋予删除数据库权限
    4.使用用户test1删除数据库
    5.创建数据库
    6.使用用户删除数据库
    7.修改用户为数据库所有者
    8.使用用户删除数据库
Expect      :
    1.创建成功
    2.删除失败
    3.创建成功
    4.删除成功
    5.创建成功
    6.删除失败
    7.修改成功
    8.删除成功
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DdlDatabaseCase0015(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Database_Case0015.py 开始执行--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.dbname = 'database_case015'
        self.username = 'userdb'
        self.password = 'test@12345'

    def test_database_case0015(self):
        self.log.info('-------------1.创建数据库-----------')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists {self.dbname};"
            f"create database {self.dbname};")
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('---2.连接该数据库，使用系统用户删除数据库---')
        sql = f'drop database if exists {self.dbname};'
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn('cannot drop the currently open database', result)

        self.log.info('---------3.创建用户并赋予删除数据库权限------------')
        sql = f"create user {self.username} with password '{self.password}';" \
            f"grant  DROP ON DATABASE {self.dbname} to {self.username};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)

        self.log.info('--------4.使用用户test1删除数据库----------')
        sql = f"drop database if exists {self.dbname}; "
        cmd = f"-U {self.username} -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, result)

        self.log.info('-------------5.创建数据库-----------')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists {self.dbname};"
            f"create database {self.dbname} ;")
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('--------6.使用用户test1删除数据库----------')
        sql = f"drop database if exists {self.dbname}; "
        cmd = f"-U {self.username} -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.PERMISSION_DENIED, result)

        self.log.info('-----7.修改用户为数据库所有者---------')
        sql = f"alter database {self.dbname} owner to {self.username};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('--------8.使用用户test1删除数据库----------')
        sql = f"drop database if exists {self.dbname}; "
        cmd = f"-U {self.username} -W {self.password}"
        result = self.commonshpri.execut_db_sql(sql, cmd)
        self.log.info(result)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, result)

    def tearDown(self):
        self.log.info('--------------------环境清理------------------')
        self.log.info('----------删除数据库--------')
        sql = f"drop database if exists {self.dbname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('----------删除用户--------')
        sql = f"drop user if exists {self.username};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('---Opengauss_Function_DDL_Database_Case0015.py 执行结束--')
