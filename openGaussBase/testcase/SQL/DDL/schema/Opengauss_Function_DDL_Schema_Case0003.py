"""
Case Type   : 基础功能
Case Name   : 创建模式时创建对象
Description :
    1. 创建模式时创建分区表，分区索引及视图
    2.插入数据，并查看
    3.创建用户
    4.创建模式时创建表，用户,并赋值
    5.创建模式时创建group
    6.创建模式时创建role
    7.创建模式时创建user
    8.创建模式时创建SEQUENC
    9.创建模式时创建DATA SOURCE
    10.创建模式时创建DIRECTORY
    11.创建模式时创建MATERIALIZED VIEW
    12.创建模式时创建database
    13.创建模式时创建TABLESPACE
    14.创建模式时创建SEQUENCE
    15.创建函数
    16.创建模式时创建触发器
    17.使用触发器
    18.修改enable_incremental_checkpoint=off
    19.创建模式时创建外表
Expect      :
    1.创建成功
    2.插入数据成功，且可以查询
    3.创建用户成功
    4.创建成功，且赋权成功
    5.创建失败
    6.创建失败
    7.创建失败
    8.创建成功
    9.创建失败
    10.创建失败
    11.创建失败
    12.创建失败
    13.创建失败
    14.创建成功
    15.创建成功
    16.创建成功
    17.触发器生效
    18.配置成功
    19.创建失败
History     :
"""

import unittest
import time
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DdlDatabase(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Schema_Case0003.py start--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.schname = 'schema_case003'
        self.tablename = 'tbl_case003'
        self.indexname = 'idx_case003'
        self.viewname = 'view_case003'
        self.username = 'user_case003'
        self.password = macro.COMMON_PASSWD
        self.comm = Common()

    def test_basebackup(self):
        self.log.info('------1.创建模式时创建分区表，分区索引及视图-------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname} " \
            f"create table {self.tablename}(i int)partition " \
            f"by list(i)(partition p1 values(1234)) " \
            f"create index {self.indexname} on " \
            f"{self.tablename}(i) local (PARTITION p1)" \
            f" create view {self.viewname} as select * from {self.tablename};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------2.插入数据，并查看----')
        sql = f"insert into {self.schname}.{self.tablename} values(1234);" \
            f"select * from {self.schname}.{self.tablename} where i<10000;" \
            f"explain select * from {self.schname}.{self.tablename} " \
            f"where i<10000;select * from {self.schname}.{self.viewname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
        self.assertIn('1234', result)
        self.assertIn(self.indexname, result)
        sql = f"select * from {self.schname}.{self.viewname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('1234', result)

        self.log.info('--------3.创建用户----------------')
        sql = f"create user {self.username} with password '{self.password}';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)

        self.log.info('--------4.创建模式时创建表，用户,并赋值----------------')
        sql = f'drop schema if exists {self.schname} CASCADE;' \
            f'create schema {self.schname} ' \
            f'create table {self.tablename}(i int) ' \
            f'WITH (ORIENTATION = COLUMN)' \
            f'  grant all privileges to {self.username};'
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------5.创建模式时创建group-------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname} " \
            f"CREATE GROUP test_group PASSWORD '{self.password}';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------6.创建模式时创建role-------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname} " \
            f"CREATE role test_role PASSWORD '{self.password}';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------7.创建模式时创建user-------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname} " \
            f"CREATE user test_user PASSWORD '{self.password}';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------8.创建模式时创建SEQUENC-------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname} " \
            f"create SEQUENCE serial START 101 CACHE 20;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------9.创建模式时创建DATA SOURCE -------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname}" \
            f" CREATE DATA SOURCE ds_test2 TYPE 'MPPDB' VERSION NULL;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------10.创建模式时创建DIRECTORY -------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname} " \
            f"CREATE OR REPLACE DIRECTORY  dir  " \
            f"as '/openGauss/liumin0113/cluster/dn1';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------11.创建模式时创建MATERIALIZED VIEW -------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname} " \
            f"create table {self.tablename}(i int) " \
            f"create  MATERIALIZED view {self.viewname}" \
            f" as select * from sql_test1;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------12.创建模式时创建database -------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname} create database test;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------13.创建模式时创建TABLESPACE -------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname}  " \
            f"CREATE TABLESPACE ds_location1 RELATIVE " \
            f"LOCATION 'tablespace/tablespace_1';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------14.创建函数 -------')
        sql = f"CREATE OR REPLACE FUNCTION tri_insert_func() " \
            f"RETURNS TRIGGER AS  " \
            f"\$\$   " \
            f"DECLARE   " \
            f"BEGIN  " \
            f"INSERT INTO test_trigger_des_tbl " \
            f"VALUES(NEW.id1, NEW.id2, NEW.id3);  " \
            f"RETURN NEW;      " \
            f"END           " \
            f"\$\$ LANGUAGE PLPGSQL;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, result)

        self.log.info('------15.创建模式时创建触发器-------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname} " \
            f"CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT)" \
            f" CREATE TRIGGER insert_trigger " \
            f"  BEFORE INSERT ON test_trigger_src_tbl" \
            f"  FOR EACH ROW " \
            f" EXECUTE PROCEDURE tri_insert_func();"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('------16.使用触发器-------')
        sql = f"CREATE TABLE test_trigger_des_tbl" \
            f"(id1 INT, id2 INT, id3 INT);" \
            f"INSERT INTO {self.schname}.test_trigger_src_tbl" \
            f" VALUES(100,200,300);" \
            f"SELECT * FROM test_trigger_des_tbl;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(' 100 | 200 | 300', result)

        self.log.info('-----17.修改enable_incremental_checkpoint=off-------')
        sql = f"ALTER SYSTEM SET enable_incremental_checkpoint TO off;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('ALTER SYSTEM SET', result)
        result = self.commonshpri.stop_db_cluster()
        self.assertTrue(result)
        result = self.commonshpri.start_db_cluster(True)
        self.log.info(result)
        self.assertTrue(self.constant.START_SUCCESS_MSG
                        in result or 'Degrade' in result)

        self.log.info('------18.创建模式时创建外表 -------')
        sql = f"drop schema if exists {self.schname} CASCADE;" \
            f"create schema {self.schname} create foreign table test(x int);"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)
        self.assertIn('error at or near "foreign"', result)

    def tearDown(self):
        self.log.info('------------环境清理-----------')
        self.log.info("----------删除表-----------")
        result = self.commonshpri.execut_db_sql(
            "drop table if exists test_trigger_des_tbl cascade;"
            "drop table if exists test_trigger_src_tbl cascade;")
        self.log.info(result)
        self.log.info('---------删除数据库------')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists test;")
        self.log.info(result)

        self.log.info('---------删除模式------')
        result = self.commonshpri.execut_db_sql(
            f"drop schema if exists {self.schname} CASCADE;")
        self.log.info(result)

        self.log.info('---------删除用户------')
        result = self.commonshpri.execut_db_sql(
            f"drop user if exists {self.username};")
        self.log.info(result)

        self.log.info('-------删除函数---------')
        result = self.commonshpri.execut_db_sql(
            f"DROP FUNCTION IF EXISTS tri_insert_func;")
        self.log.info(result)

        self.log.info('-------删除序列---------')
        result = self.commonshpri.execut_db_sql(
            f"DROP SEQUENCE serial;")
        self.log.info(result)

        self.log.info('-----------备机重建----------------')
        if self.comm.get_node_num(self.db_primary_db_user) > 2:
            CommonSH('Standby1DbUser').build_standby()
            CommonSH('Standby2DbUser').build_standby()

        self.log.info('-----修改enable_incremental_checkpoint=on-------')
        sql = f"ALTER SYSTEM SET enable_incremental_checkpoint TO on;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        result = self.commonshpri.stop_db_cluster()
        self.log.info(result)
        result = self.commonshpri.start_db_cluster(True)
        self.log.info(result)
        time.sleep(10)

        self.log.info('--Opengauss_Function_DDL_Schema_Case0003.py finish-')
