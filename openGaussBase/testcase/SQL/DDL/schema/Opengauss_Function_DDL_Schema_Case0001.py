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
Case Name   : 创建schema使用不同名称
Description :
    1.创建schema使用合法名称
    2. 相同数据库创建同名schema
    3.创建数据库
    4.在不同数据库下创建相同名称schema
    5.创建schema名称为数字
    6.创建schema名称为pg_开头
    7.创建schema名称不符合表示符规范
Expect      :
    1.创建成功
    2.创建失败，合理报错
    3.创建成功
    4.创建成功
    5.创建失败，合理报错
    6.创建失败合理报错
    7.创建失败合理报错
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DdlDatabase(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Schema_Case0001.py start--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.dbname = 'database_case001'
        self.schname = 'schema_case001'

    def test_basebackup(self):
        self.log.info('------1..创建schema使用合法名称-------')
        sql = f"drop schema if exists {self.schname};" \
              f"create schema {self.schname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------2. 相同数据库创建同名schema----')
        sql = f"create schema {self.schname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('already exists', result)

        self.log.info('------3.创建数据库称-------')
        sql = f"drop database if exists {self.dbname};" \
              f"create database {self.dbname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('------4.在不同数据库下创建相同名称schema-------')
        sql = f"create schema {self.schname};"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------5.创建schema名称为数字----')
        sql = f"create schema 1234567;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('error at or near "1234567"', result)

        self.log.info('------6.创建schema名称为pg_开头----')
        sql = f"create schema pg_test;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.constant.CREATE_TABLE_SUCCESS, result)

        self.log.info('------7.创建schema名称不符合表示符规范----')
        sql = f"create schema 123test;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('error at or near "123"', result)

    def tearDown(self):
        self.log.info('------------环境清理-----------')
        self.log.info('---------删除数据库------')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists {self.dbname};")
        self.log.info(result)

        self.log.info('---------删除模式------')
        result = self.commonshpri.execut_db_sql(
            f"drop schema if exists {self.schname};")
        self.log.info(result)

        self.log.info('--Opengauss_Function_DDL_Schema_Case0001.py finish-')
