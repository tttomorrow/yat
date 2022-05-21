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
Case Name   : 创建数据库使用不同兼容模式
Description :
    1.创建兼容oracle数据库
    2.创建表，并插入数据
    3.创建数据库兼容mysql
    4.创建表，并插入数据
    5.创建数据库兼容TD
    6..创建表，并插入数据
    7.创建数据库兼容PG
    8..创建表，并插入数据
    9.查看数据库默认所有者
    10.兼容模式为异常值
Expect      :
    1.创建数据库成功
    2.创建表成功，插入数据'你好呀'提示value too long for type character(3),
    空字符串也为null,字符转换为整数报错
    3.创建数据库成功
    4.创建表成功空字符串不等于null，字符转整数为0
    5.创建数据库成功
    6.创建表成功空字符串不等于null，字符转整数报错
    7.创建数据库成功
    8.创建表并插入数据成功，空字符串不等于NULL，字符转整型报错
    9.数据库默认所有者为当前用户
    10.创建数据库失败
History     :
"""

import unittest
import sys
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DdlDatabase(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Database_Case0003.py start--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.dbname = 'database_case003'
        self.tblname = 'tbl_case003'
        self.errorlog = 'ERROR:  invalid input syntax for integer'

    def test_basebackup(self):
        self.log.info('------1.创建兼容oracle数据库-------')
        sql = f"drop database if exists {self.dbname};\
        create database {self.dbname} with DBCOMPATIBILITY ='A'  " \
            f"TEMPLATE=template0 ENCODING='UTF8';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('------2.创建表，并插入数据----')
        sql = f'create table {self.tblname}(i char(3), x varchar );'
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)
        sql = f"insert into {self.tblname} values('你好呀','%');"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn("value too long for type character(3)", result)
        sql = f"insert into {self.tblname} values(NULL,'%')," \
            f"('','*'),('hi','你好');" \
            f"select * from {self.tblname} where i is null;"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
        self.assertIn('   | %', result)
        self.assertIn('   | *', result)
        sql = f"select cast('你' as integer ) ;"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.errorlog, result)

        self.log.info('---------3.创建数据库兼容mysql------')
        sql = f"drop database if exists {self.dbname};" \
            f"create database {self.dbname} with" \
            f" DBCOMPATIBILITY ='B'" \
            f" TEMPLATE=template0 ENCODING='UTF8'"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('------4.创建表，并插入数据----')
        sql = f'create table {self.tblname}(i char(3), x varchar );'
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)
        sql = f"insert into {self.tblname} values(NULL,'%')," \
            f"('','*'),('hi','你好');" \
            f"select * from {self.tblname} where i is null;"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
        self.assertIn('   | %', result)
        self.assertNotIn('   | *', result)
        sql = f"select cast('你' as integer ) ;"
        result = self.commonshpri.execut_db_sql(sql,
                                                dbname=self.dbname)
        self.log.info(result)
        self.assertIn('int4', result)
        self.assertIn('0', result)

        self.log.info('---------5.创建数据库兼容TD------')
        sql = f"drop database if exists {self.dbname};" \
            f"create database {self.dbname} with DBCOMPATIBILITY ='C' " \
            f"TEMPLATE=template0 ENCODING='UTF8'"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('------6.创建表，并插入数据----')
        sql = f'create table {self.tblname}(i char(3), x varchar );'
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)
        sql = f"insert into {self.tblname} values(NULL,'%')," \
            f"('','*'),('hi','你好');" \
            f"select * from {self.tblname} where i is null;"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
        self.assertIn('   | %', result)
        self.assertNotIn('   | *', result)
        sql = f"select cast('你' as integer ) ;"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.errorlog, result)

        self.log.info('--------7.创建数据库兼容PG------')
        sql = f"drop database if exists {self.dbname};" \
            f"create database {self.dbname} with " \
            f"DBCOMPATIBILITY ='PG' TEMPLATE=template0 ENCODING='UTF8'"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('------8.创建表，并插入数据----')
        sql = f'create table {self.tblname}(i char(3), x varchar );'
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)
        sql = f"insert into {self.tblname} values(NULL,'%')," \
            f"('','*'),('你好呀','你好');" \
            f"select * from {self.tblname} where i is null;"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
        self.assertNotIn('value too long for type character(3)', result)
        self.assertIn('   | %', result)
        self.assertNotIn('   | *', result)
        sql = f"select cast('你' as integer ) ;"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.errorlog, result)
        self.log.info('----------9.查看数据库默认所有者-------')
        result = self.commonshpri.execut_db_sql(f'\l')
        self.log.info(result)
        db_lists = result.strip().splitlines()
        flag = True
        for i in db_lists:
            if self.dbname in i:
                db_info = i.strip().split('|')[1]
                self.assertIn(self.db_primary_db_user.ssh_user, db_info)
                flag = False
                break
        self.assertFalse(flag)

        self.log.info('----------10.兼容模式为异常值-----')
        sql = f"drop database if exists {self.dbname};" \
            f"create database {self.dbname} " \
            f"with DBCOMPATIBILITY ='P' TEMPLATE=template0 ENCODING='UTF8'"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('ERROR:  Compatibility args P is invalid', result)

    def tearDown(self):
        self.log.info('------------环境清理-----------')
        self.log.info('---------删除数据库------')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists {self.dbname};")
        self.log.info(result)

        self.log.info('--Opengauss_Function_DDL_Database_Case0003.py finish-')
