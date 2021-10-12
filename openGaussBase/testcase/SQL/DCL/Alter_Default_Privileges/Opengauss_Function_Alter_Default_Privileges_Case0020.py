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
Case Name   : 无权限用户自己alter自己权限
Description :
    1.无权限用户alter自己的权限 期望:不带模式的alter不报错，alter不生效，查询权限不变
    1.1.管理员用户连接创建无权限用户 default020_02 期望:创建成功
    1.2.default020_02用户连接 执行alter测试
    1.1.清理 期望:清理成功
    备注:以上alter测试包括对表（包含视图），类型，函数的权限测试
Expect      :
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
        logger.info('--------Opengauss_Function_Alter_Default_Privileges_Case0020开始执行--------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_common_user_permission(self):
        logger.info('--------1.无权限用户alter自己的权限 --------')
        logger.info('--------1.1.管理员用户连接创建无权限用户 default020_02--------')
        sql_cmd = commonsh.execut_db_sql(f'''
                                        drop owned by default020_02 cascade;
                                        drop role if exists default020_02;
                                        create role default020_02 password '{macro.COMMON_PASSWD}';
                                        alter role default020_02 with login;
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)

        logger.info('--------1.2.default020_02用户连接 执行alter测试--------')
        sql_cmd = ('''
                    drop schema if exists schema_020 cascade;
                    create schema schema_020;
                    ALTER DEFAULT PRIVILEGES for role default020_02 in schema schema_020 GRANT ALL PRIVILEGES on tables to default020_02 WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role default020_02 GRANT select,insert,update,truncate,references,TRIGGER,DELETE on tables to default020_02 WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role default020_02 in schema schema_020 GRANT ALL PRIVILEGES on functions to default020_02 WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role default020_02 GRANT EXECUTE  on functions to default020_02 WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role default020_02 in schema schema_020 GRANT ALL PRIVILEGES on TYPES to default020_02 WITH GRANT OPTION ;
                    ALTER DEFAULT PRIVILEGES for role default020_02 GRANT USAGE  on TYPES to default020_02 WITH GRANT OPTION ;

                    drop schema if exists schema_020 cascade;
                    create schema schema_020;
                    drop table if exists test_alter_default_020 cascade;
                    create table  test_alter_default_020(id int unique);
                    select * from test_alter_default_020;
                    drop function if exists test_default_020(int) cascade;
                    create or replace function test_default_020(a int) return int
                    as
                    b int:= a;
                    begin
                        for i in 1..a loop
                            b:=b+1;
                        end loop;
                        return b;
                    end;
                    
                    select test_default_020(16);
                    drop type if exists type020;
                    CREATE TYPE type020 AS (c_int int,c_text text);
                    drop table if exists test_alter_default_020 cascade;
                    create table  test_alter_default_020(id type020);
                    select * from test_alter_default_020;
                                        
                    ALTER DEFAULT PRIVILEGES for role default020_02 in schema schema_020 revoke ALL on tables from default020_02 CASCADE CONSTRAINTS ;
                    ALTER DEFAULT PRIVILEGES for role default020_02 revoke select,insert,update,truncate,references,TRIGGER,DELETE on tables from default020_02 CASCADE CONSTRAINTS;
                    ALTER DEFAULT PRIVILEGES for role default020_02 in schema schema_020 revoke ALL on functions from default020_02 CASCADE CONSTRAINTS ;
                    ALTER DEFAULT PRIVILEGES for role default020_02 revoke EXECUTE  on functions from default020_02 CASCADE CONSTRAINTS;
                    ALTER DEFAULT PRIVILEGES for role default020_02 in schema schema_020 revoke ALL on TYPES from default020_02 CASCADE CONSTRAINTS ;
                    ALTER DEFAULT PRIVILEGES for role default020_02 revoke USAGE  on TYPES from default020_02 CASCADE CONSTRAINTS;
                    ''')
        excute_cmd = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default020_02 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                            '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg)

        logger.info('--------1.1.清理--------')
        sql_cmd = commonsh.execut_db_sql('''
                                        drop owned by default020_02 cascade;
                                        drop user if exists default020_02;
                                        ''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)

    def tearDown(self):
        logger.info('--------清理环境 no need to clean--------')
        logger.info('--------1.1.清理--------')
        sql_cmd = commonsh.execut_db_sql('''
                                        drop owned by default020_02 cascade;
                                        drop user if exists default020_02;
                                        ''')
        logger.info(sql_cmd)
        logger.info('--------Opengauss_Function_Alter_Default_Privileges_Case0020执行结束--------')