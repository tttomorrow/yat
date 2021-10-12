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
Case Name   : 修改模式用户
Description :
    1.创建数据库
    2.创建schema
    3.删除数据库test的public
    4.创建public schema ，并赋权限
    5.检查public权限
    6.创建表
    7.查看table模式
Expect      :
    1.创建数据库成功
    2.创建schema成功
    3.删除public成功
    4.创建成功
    5.权限为包含UC +U
    6.创建表成功
    7.table模式为public
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Ddlschema(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Schema_Case0010.py start--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.schema_name = 'schema_case010'
        self.dbname = 'db_case010'
        self.tbname = 'tb_case010'

    def test_schema(self):
        self.log.info('----------------1.创建数据库-----------------')
        sql = f"create database {self.dbname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('-------------2.创建schema---------------------')
        sql = f"create schema {self.schema_name};"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('-------------3.删除public成功---------------------')
        sql = f"drop schema public"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.DROP_SCHEMA_SUCCESS_MSG, result)

        self.log.info('-----------4.创建public schema ，并赋权限-------------')
        sql = f"create schema public;" \
            f"GRANT ALL ON SCHEMA public " \
            f"TO {self.db_primary_db_user.ssh_user};" \
            f"GRANT USAGE  ON SCHEMA public TO public;"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------------5.权限为包含UC +U---------')
        result = self.commonshpri.execut_db_sql(
            r'\dnS+ public', dbname=self.dbname)
        self.log.info(result)
        self.assertIn(f'{self.db_primary_db_user.ssh_user}=UC', result)
        self.assertIn(r'=U/', result)

        self.log.info('---------------6.创建表成功--------------')
        sql = f'create table {self.tbname}(i int);'
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)

        self.log.info('---------7.查看table模式---------')
        sql = f'\d {self.tbname}'
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn('public', result)

    def tearDown(self):
        self.log.info('------------环境清理-----------')
        self.log.info('---------删除数据库------')
        sql = f"drop database if exists {self.dbname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('--Opengauss_Function_DDL_Schema_Case0010.py finish-')
