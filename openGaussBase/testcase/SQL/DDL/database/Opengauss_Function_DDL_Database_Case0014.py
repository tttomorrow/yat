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
Case Name   : 修改数据库隔离级别
Description :
    1.创建用户
    2.创建数据库
    3.连接数据库test对用户A赋予权限
    4.使用系统用户创建表，及视图
    5.使用用户A在数据库中创建表和视图
    6.使用用户A连接数据库test查看该数据库中存在表及视图
    7.修改数据库隔离级别
    8.使用用户A查看test中表和视图
    9.使用系统用户查看test中表和视图
    10.修改隔离级别
    11.使用用户A查看test中表和视图
    12.修改隔离级别为非法参数
Expect      :
    1.创建成功
    2.创建成功
    3.赋权成功
    4.创建表成功
    5.创建表成功
    6.可以查到系统用户的表和视图
    7.修改隔离级别成功
    8.A用户无法查看系统用户创建的表和视图
    9.系统用户可以查询所有表和视图
    10.修改隔离级别成功
    11.可以查到系统用户的表和视图
    12.修改失败
History     :
"""

import unittest
import sys
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DdlDatabaseCase0014(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Database_Case0014.py 开始执行--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.dbname = 'database_case014'
        self.tblname = 'tbl_case014'
        self.viewname = 'mv_view'
        self.tblname1 = 'table014'
        self.viewname1 = 'view014'
        self.username = 'user1'
        self.password = 'test@12345'

    def test_database_case0014(self):
        self.log.info('---------1.创建用户------------')
        sql = f"create user {self.username} with password '{self.password}';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)

        self.log.info('-------------2.创建数据库-----------')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists {self.dbname};"
            f"create database {self.dbname} with owner {self.username};")
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('---3.连接数据库test对用户A赋予权限--')
        sql = f"grant CREATE on schema public to {self.username};"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, result)

        self.log.info('---------4.使用系统用户创建表，及视图-----------')
        sql = f"create table {self.tblname}(i int);" \
            f"insert into {self.tblname} values(999);" \
            f"CREATE MATERIALIZED VIEW {self.viewname} " \
            f"as table {self.tblname};"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
        self.assertIn('CREATE MATERIALIZED VIEW', result)

        self.log.info('---------5.使用用户A在数据库中创建表和视图-----------')
        sql = f"create table {self.tblname1}(i int);" \
            f"insert into {self.tblname1} values(999);" \
            f"CREATE MATERIALIZED VIEW {self.viewname1} " \
            f"as table {self.tblname1};"
        cmd = f'-U {self.username} -W {self.password}'
        result = self.commonshpri.execut_db_sql(sql, cmd, self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
        self.assertIn('CREATE MATERIALIZED VIEW', result)

        self.log.info('----6.使用用户A连接数据库test查看该数据库中存在表及视图----')
        cmd = f'-U {self.username} -W {self.password}'
        result = self.commonshpri.execut_db_sql(r'\d', cmd, self.dbname)
        self.log.info(result)
        self.assertIn(self.tblname, result)
        self.assertIn(self.tblname1, result)
        result = self.commonshpri.execut_db_sql(r'\dp', cmd, self.dbname)
        self.log.info(result)
        self.assertIn(self.viewname, result)
        self.assertIn(self.viewname1, result)

        self.log.info('---------7.修改数据库隔离级别-----------')
        sql = f"alter database {self.dbname} WITH ENABLE PRIVATE OBJECT;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('----------8.使用用户A查看test中表和视图-----------')
        cmd = f'-U {self.username} -W {self.password}'
        result = self.commonshpri.execut_db_sql(r'\d', cmd, self.dbname)
        self.log.info(result)
        self.assertNotIn(self.tblname, result)
        self.assertIn(self.tblname1, result)
        result = self.commonshpri.execut_db_sql(r'\dp', cmd, self.dbname)
        self.log.info(result)
        self.assertNotIn(self.viewname, result)
        self.assertIn(self.viewname1, result)

        self.log.info('----------9.使用系统用户查看test中表和视图-----------')
        result = self.commonshpri.execut_db_sql(r'\d', '', self.dbname)
        self.log.info(result)
        self.assertIn(self.tblname, result)
        self.assertIn(self.tblname1, result)
        result = self.commonshpri.execut_db_sql(r'\dp', '', self.dbname)
        self.log.info(result)
        self.assertIn(self.viewname, result)
        self.assertIn(self.viewname1, result)

        self.log.info('---------10.修改数据库隔离级别-----------')
        sql = f"alter database {self.dbname} WITH DISABLE PRIVATE OBJECT;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('----------11.使用用户A查看test中表和视图-----------')
        cmd = f'-U {self.username} -W {self.password}'
        result = self.commonshpri.execut_db_sql(r'\d', cmd, self.dbname)
        self.log.info(result)
        self.assertIn(self.tblname, result)
        self.assertIn(self.tblname1, result)
        result = self.commonshpri.execut_db_sql(r'\dp', cmd, self.dbname)
        self.log.info(result)
        self.assertIn(self.viewname, result)
        self.assertIn(self.viewname1, result)

        self.log.info('---------12.修改隔离级别为非法参数 -----------')
        sql = f"alter database {self.dbname} WITH off PRIVATE OBJECT;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertNotIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

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
        self.log.info('---Opengauss_Function_DDL_Database_Case0014.py 执行结束--')
