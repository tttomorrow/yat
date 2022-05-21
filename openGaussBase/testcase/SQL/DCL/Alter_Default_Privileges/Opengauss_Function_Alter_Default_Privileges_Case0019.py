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
Case Type   : 功能测试
Case Name   : 在事务中进行alter
Description :
    1.管理员用户连接 创建用户 期望:创建成功
    2.管理员用户连接 在事务中进行赋权 期望:赋权成功
    3.管理员用户连接 创建type 表和函数，查询赋权是否成功 期望:创建成功，赋权成功，count(*)不为0
    4.管理员用户连接 在事务中进行权限回收 期望:权限回收
    5.管理员用户连接 创建type 表和函数，查询权限回收是否成功 期望:创建成功，权限回收成功，count(*)为0
    6.管理员用户连接 清理环境 期望:清理成功
Expect      :
History     :
"""

import sys
import unittest
from yat.test import macro
from yat.test import Node
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('----------------------Opengauss_Function_Alter_Default_Privileges_Case0019执行开始--------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_common_user_permission(self):
        logger.info('------------------------管理员用户连接，创建用户，赋登录权限，建表 期望:创建成功-----------------------------')
        sql_cmd = commonsh.execut_db_sql(f'''
                                        drop owned by default019_01 cascade;
                                        drop role if exists default019_01;
                                        create role default019_01 password '{macro.COMMON_PASSWD}';
                                        alter role default019_01 with login;
                                        grant all privileges to default019_01;
                                        drop schema if exists schema_019 cascade;
                                        create schema schema_019;
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.CREATE_SCHEMA_SUCCESS_MSG, sql_cmd)

        logger.info('------------------------管理员用户连接 在事务中进行赋权 期望:赋权成功-----------------------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        START TRANSACTION;
                                            ALTER DEFAULT PRIVILEGES in schema schema_019 GRANT ALL PRIVILEGES on tables to default019_01 WITH GRANT OPTION ;
                                            ALTER DEFAULT PRIVILEGES GRANT select,insert,update,truncate,references,TRIGGER,DELETE on tables to default019_01 WITH GRANT OPTION ;
                                            ALTER DEFAULT PRIVILEGES in schema schema_019 GRANT ALL PRIVILEGES on functions to default019_01 WITH GRANT OPTION ;
                                            ALTER DEFAULT PRIVILEGES GRANT EXECUTE  on functions to default019_01 WITH GRANT OPTION ;
                                            ALTER DEFAULT PRIVILEGES in schema schema_019 GRANT ALL PRIVILEGES on TYPES to default019_01 WITH GRANT OPTION ;
                                            ALTER DEFAULT PRIVILEGES GRANT USAGE  on TYPES to default019_01 WITH GRANT OPTION ;
                                        end;
                                        ''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)

        logger.info('-------------管理员用户连接 创建type 表和函数，查询赋权是否成功 期望:创建成功，赋权成功，count(*)不为0--------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        drop schema if exists schema_019 cascade;
                                        create schema schema_019;
                                        drop table if exists test_alter_default_019 cascade;
                                        create table  test_alter_default_019(id int unique);
                                        select * from test_alter_default_019;
                                        drop function if exists test_default_019(int) cascade;
                                        create or replace function test_default_019(a int) return int
                                        as
                                        b int:= a;
                                        begin
                                            for i in 1..a loop
                                                b:=b+1;
                                            end loop;
                                            return b;
                                        end;
                                        select test_default_019(16);
                                        drop type if exists type019;
                                        CREATE TYPE type019 AS (c_int int,c_text text);
                                        drop table if exists test_alter_default_019 cascade;
                                        create table  test_alter_default_019(id type019);
                                        select * from test_alter_default_019;
                                        ''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        sql_cmd = commonsh.execut_db_sql('''
                                        select count(*) from information_schema.table_privileges where grantee='default019_01';
                                        ''')
        logger.info(sql_cmd)
        self.assertTrue(int(sql_cmd.split('\n')[-2]) > 0)

        logger.info('------------------------管理员用户连接 在事务中进行权限回收 期望:权限回收-----------------------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        START TRANSACTION;
                                        ALTER DEFAULT PRIVILEGES in schema schema_019 revoke ALL on tables from default019_01 CASCADE CONSTRAINTS ;
                                        ALTER DEFAULT PRIVILEGES revoke select,insert,update,truncate,references,TRIGGER,DELETE on tables from default019_01 CASCADE CONSTRAINTS;
                                        ALTER DEFAULT PRIVILEGES in schema schema_019 revoke ALL on functions from default019_01 CASCADE CONSTRAINTS ;
                                        ALTER DEFAULT PRIVILEGES revoke EXECUTE  on functions from default019_01 CASCADE CONSTRAINTS;
                                        ALTER DEFAULT PRIVILEGES in schema schema_019 revoke ALL on TYPES from default019_01 CASCADE CONSTRAINTS ;
                                        ALTER DEFAULT PRIVILEGES revoke USAGE  on TYPES from default019_01 CASCADE CONSTRAINTS;
                                        end;
                                        ''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)

        logger.info('-------------管理员用户连接 创建type 表和函数，查询权限回收是否成功 期望:创建成功，权限回收成功，count(*)为0--------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        drop schema if exists schema_019 cascade;
                                        create schema schema_019;
                                        drop table if exists test_alter_default_019 cascade;
                                        create table  test_alter_default_019(id int unique);
                                        select * from test_alter_default_019;
                                        drop function if exists test_default_019(int) cascade;
                                        create or replace function test_default_019(a int) return int
                                        as
                                        b int:= a;
                                        begin
                                            for i in 1..a loop
                                                b:=b+1;
                                            end loop;
                                            return b;
                                        end;
                                        
                                        select test_default_019(16);
                                        drop type if exists type019;
                                        CREATE TYPE type019 AS (c_int int,c_text text);
                                        drop table if exists test_alter_default_019 cascade;
                                        create table  test_alter_default_019(id type019);
                                        select * from test_alter_default_019;
                                        ''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)

        sql_cmd = commonsh.execut_db_sql('''
                                        select count(*) from information_schema.table_privileges where grantee='default019_01';
                                        ''')
        logger.info(sql_cmd)
        self.assertTrue("0" in sql_cmd.split('\n')[-2], )

        logger.info('-----------------------------------管理员用户连接 清理环境 期望:清理成功-----------------------------------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        drop type if exists type019 cascade;
                                        drop table if exists test_alter_default_019 cascade;
                                        drop function if exists test_default_019(int) cascade;
                                        drop schema if exists schema_019 cascade;
                                        drop owned by default019_01 cascade;
                                        drop role if exists default019_01;
                                        ''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, sql_cmd)
        self.assertIn(self.Constant.DROP_FUNCTION_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        logger.info('------------------------------------------清理环境 no need to clean---------------------------------------------')
        logger.info('-------------------------Opengauss_Function_Alter_Default_Privileges_Case0019执行结束---------------------------')