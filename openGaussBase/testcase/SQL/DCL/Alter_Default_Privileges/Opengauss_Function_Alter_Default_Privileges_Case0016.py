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
Case Type   : 功能测试
Case Name   : 初始用户和sysadmin自己alter自己权限
Description :
    1.初始用户alter自己的权限:alter不报错，但不生效，查询权限不变
    1.1.初始用户alter自己的权限
    1.2.清理环境 期望:清理成功
    2.sysadmin用户alter自己的权限:alter不报错，但不生效，查询权限不变
    2.1.管理员用户连接创建sysadmin用户 default016_01 期望:创建成功
    2.2.default016_016用户连接 执行alter测试
    2.3.清理 期望:清理成功
    备注:以上alter测试包括对表（包含视图），类型，函数的权限测试
Expect      :
    1.初始用户alter自己的权限:alter不报错，但不生效，查询权限不变
    1.1.初始用户alter自己的权限
    1.2.清理环境 期望:清理成功
    2.sysadmin用户alter自己的权限:alter不报错，但不生效，查询权限不变
    2.1.管理员用户连接创建sysadmin用户 default016_01 期望:创建成功
    2.2.default016_016用户连接 执行alter测试
    2.3.清理 期望:清理成功
    备注:以上alter测试包括对表（包含视图），类型，函数的权限测试
History     :
"""

import sys
import unittest
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
logger = Logger()
commonsh = CommonSH('dbuser')

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('--------Opengauss_Function_Alter_Default_Privileges_Case0016开始执行--------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        # 初始用户用户名
        self.username = self.userNode.ssh_user
        # 初始用户密码
        self.password = macro.GAUSSDB_INIT_USER_PASSWD

    def test_common_user_permission(self):
        logger.info('--------1.初始用户alter自己的权限--------')
        logger.info('--------1.1.初始用户alter自己的权限--------')
        sql_cmd = (f'''
                    drop schema if exists schema_016 cascade;
                    create schema schema_016;
                    ALTER DEFAULT PRIVILEGES for role {self.username} in schema schema_016 GRANT ALL PRIVILEGES on tables to {self.username} WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role {self.username} GRANT select,insert,update,truncate,references,TRIGGER,DELETE on tables to {self.username} WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role {self.username} in schema schema_016 GRANT ALL PRIVILEGES on functions to {self.username} WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role {self.username} GRANT EXECUTE  on functions to {self.username} WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role {self.username} in schema schema_016 GRANT ALL PRIVILEGES on TYPES to {self.username} WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role {self.username} GRANT USAGE  on TYPES to {self.username} WITH GRANT OPTION ;

                    drop schema if exists schema_016 cascade;
                    create schema schema_016;
                    drop table if exists test_alter_default_016 cascade;
                    create table  test_alter_default_016(id int unique);
                    select * from test_alter_default_016;
                    drop function if exists test_default_016(int) cascade;
                    create or replace function test_default_016(a int) return int
                    as
                    b int:= a;
                    begin
                        for i in 1..a loop
                            b:=b+1;
                        end loop;
                        return b;
                    end;
                    
                    select test_default_016(16);
                    drop type if exists type016;
                    CREATE TYPE type016 AS (c_int int,c_text text);
                    drop table if exists test_alter_default_016 cascade;
                    create table  test_alter_default_016(id type016);
                    select * from test_alter_default_016;
                    
                    ALTER DEFAULT PRIVILEGES for role {self.username} in schema schema_016 revoke ALL on tables from {self.username} CASCADE CONSTRAINTS ;
                    ALTER DEFAULT PRIVILEGES for role {self.username} revoke select,insert,update,truncate,references,TRIGGER,DELETE on tables from {self.username} CASCADE CONSTRAINTS;
                    ALTER DEFAULT PRIVILEGES for role {self.username} in schema schema_016 revoke ALL on functions from {self.username} CASCADE CONSTRAINTS ;
                    ALTER DEFAULT PRIVILEGES for role {self.username} revoke EXECUTE  on functions from {self.username} CASCADE CONSTRAINTS;
                    ALTER DEFAULT PRIVILEGES for role {self.username} in schema schema_016 revoke ALL on TYPES from {self.username} CASCADE CONSTRAINTS ;
                    ALTER DEFAULT PRIVILEGES for role {self.username} revoke USAGE  on TYPES from {self.username} CASCADE CONSTRAINTS;
                    
                    ''')
        excute_cmd = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U {self.username} -W {self.password} -c "{sql_cmd}"
                            '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, msg)

        logger.info('--------1.2.清理环境--------')
        sql_cmd = ('''
                    drop table if exists test_alter_default_016 cascade;
                    drop type if exists type016 cascade;
                    drop function if exists test_default_016(int) cascade;
                    drop schema if exists schema_016 cascade;
                    ''')
        excute_cmd = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U {self.username} -W {self.password} -c "{sql_cmd}"
                            '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('--------2.sysadmin用户alter自己的权限--------')
        logger.info('--------2.1.管理员用户连接创建sysadmin用户 default016_01 --------')
        sql_cmd = commonsh.execut_db_sql(f'''
                                        drop owned by default016_01 cascade;
                                        drop user if exists default016_01;
                                        create user default016_01 password '{macro.COMMON_PASSWD}';
                                        grant all privileges to default016_01;
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)

        logger.info('--------2.2.default016_01用户连接 执行alter测试--------')
        sql_cmd = (f'''
                    drop schema if exists schema_016 cascade;
                    create schema schema_016;
                    ALTER DEFAULT PRIVILEGES for role default016_01 in schema schema_016 GRANT ALL PRIVILEGES on tables to default016_01 WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role default016_01 GRANT select,insert,update,truncate,references,TRIGGER,DELETE on tables to default016_01 WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role default016_01 in schema schema_016 GRANT ALL PRIVILEGES on functions to default016_01 WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role default016_01 GRANT EXECUTE  on functions to default016_01 WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role default016_01 in schema schema_016 GRANT ALL PRIVILEGES on TYPES to default016_01 WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role default016_01 GRANT USAGE  on TYPES to default016_01 WITH GRANT OPTION ;

                    drop schema if exists schema_016 cascade;
                    create schema schema_016;
                    drop table if exists test_alter_default_016 cascade;
                    create table  test_alter_default_016(id int unique);
                    select * from test_alter_default_016;
                    drop function if exists test_default_016(int) cascade;
                    create or replace function test_default_016(a int) return int
                    as
                    b int:= a;
                    begin
                        for i in 1..a loop
                            b:=b+1;
                        end loop;
                        return b;
                    end;
                    
                    select test_default_016(16);
                    drop type if exists type016;
                    CREATE TYPE type016 AS (c_int int,c_text text);
                    drop table if exists test_alter_default_016 cascade;
                    create table  test_alter_default_016(id type016);
                    select * from test_alter_default_016;
                    
                    ALTER DEFAULT PRIVILEGES for role default016_01 in schema schema_016 revoke ALL on tables from default016_01 CASCADE CONSTRAINTS ;
                    ALTER DEFAULT PRIVILEGES for role default016_01 revoke select,insert,update,truncate,references,TRIGGER,DELETE on tables from default016_01 CASCADE CONSTRAINTS;
                    ALTER DEFAULT PRIVILEGES for role default016_01 in schema schema_016 revoke ALL on functions from default016_01 CASCADE CONSTRAINTS ;
                    ALTER DEFAULT PRIVILEGES for role default016_01 revoke EXECUTE  on functions from default016_01 CASCADE CONSTRAINTS;
                    ALTER DEFAULT PRIVILEGES for role default016_01 in schema schema_016 revoke ALL on TYPES from default016_01 CASCADE CONSTRAINTS ;
                    ALTER DEFAULT PRIVILEGES for role default016_01 revoke USAGE  on TYPES from default016_01 CASCADE CONSTRAINTS;
                    
                    ''')

        excute_cmd = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default016_01 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                            '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, msg)

        logger.info('--------2.3.清理--------')
        sql_cmd = commonsh.execut_db_sql(f'''
                    drop owned by default016_01 cascade;
                    drop user if exists default016_01;
                    ''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)

    def tearDown(self):
        logger.info('----------------------------------清理环境----------------------------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        drop owned by default016_01 cascade;
                                        drop user if exists default016_01;
                                        ''')
        logger.info(sql_cmd)
        logger.info('--------Opengauss_Function_Alter_Default_Privileges_Case0016执行结束--------')