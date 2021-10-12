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
Case Name   : 创建数据库指定表空间，在该数据库上创建表和索引
Description :
    1.创建表空间
    2.创建数据库
    3.在数据库上创建表和索引使用默认表空间
    4.在数据库上创建表和索引使用指定表空间
    5.查看表和索引存储位置
Expect      :
    1.创建表空间成功
    2.创建数据库成功
    3.创建表和索引成功
    4.创建表和索引成功
    5.test和test_idx表空间为为db_space
    test1和test_idx1表空间为tb_space
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DdlDatabaseCase0013(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Database_Case0013.py 开始执行--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.dbname = 'database_case013'
        self.tblname = 'tbl_case013'
        self.tblname_sp = 'tbl_case013_sp'
        self.indexname = 'idx_case013'
        self.indexname_sp = 'idx_case013_sp'
        self.dbspace = 'db_space'
        self.tbspace = 'tb_space'

    def test_database_case0006(self):
        self.log.info('---------1.创建表空间------------')
        sql = f"create tablespace {self.dbspace} RELATIVE " \
            f"LOCATION '{self.dbspace}';" \
            f"create tablespace {self.tbspace} RELATIVE " \
            f"LOCATION '{self.tbspace}';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, result)

        self.log.info('-------------2.创建数据库-----------')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists {self.dbname};"
            f"create database {self.dbname} with TABLESPACE={self.dbspace};")
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('---------3.在数据库上创建表和索引使用默认表空间-----------')
        sql = f"create table {self.tblname}(i int);" \
            f"insert into {self.tblname} values(1);" \
            f"create index {self.indexname} on {self.tblname}(i);"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS, result)

        self.log.info('---------4.在数据库上创建表和索引使用指定表空间-----------')
        sql = f"create table {self.tblname_sp}(i int) " \
            f" tablespace  {self.tbspace};" \
            f"insert into {self.tblname_sp} values(1);" \
            f"create index {self.indexname_sp} on {self.tblname_sp}(i) " \
            f"  tablespace  {self.tbspace};"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS, result)

        self.log.info('----------5.查看表和索引存储位置-----------')
        result = self.commonshpri.execut_db_sql(f'\d {self.tblname}',
                                              '', self.dbname)
        self.log.info(result)
        self.assertIn(f'"{self.indexname}" btree (i) TABLESPACE '
                      f'{self.dbspace}', result)
        sql = f" Select oid,relname from pg_class " \
            f"where relname = '{self.tblname}';"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        oid = result.splitlines()[2]
        sql = f"Select pg_relation_filepath({oid.split('|')[0]}::regclass);"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        cmd = f"ls -al {macro.DB_INSTANCE_PATH}/pg_tblspc " \
            f"| grep {result.splitlines()[2].split('/')[1]}"
        self.log.info(cmd)
        result = self.db_primary_db_user.sh(cmd).result()
        self.log.info(result)
        self.assertIn(self.dbspace, result)

        result = self.commonshpri.execut_db_sql(f'\d {self.tblname_sp}',
                                              '', self.dbname)
        self.log.info(result)
        self.assertIn(f'"{self.indexname_sp}" btree (i) '
                      f'TABLESPACE {self.tbspace}, '
                      f'tablespace "{self.tbspace}"', result)
        sql = f"select tablespace from PG_TABLES " \
            f"where tablename='{self.tblname_sp}';"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn(self.tbspace, result)

    def tearDown(self):
        self.log.info('--------------------环境清理------------------')
        self.log.info('----------删除数据库--------')
        sql = f"drop database if exists {self.dbname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('----------删除表空间--------')
        sql = f"drop tablespace if exists {self.dbspace};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        sql = f"drop tablespace if exists {self.tbspace};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('---Opengauss_Function_DDL_Database_Case0013.py 执行结束--')
