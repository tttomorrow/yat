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
Case Name   : 无权限用户alter超级用户和sysadmin的权限
Description :
    1.初始用户连接创建用户 default018_01,default018_02 期望:创建成功
    2.无权限用户default018_02连接，for role default018_02 alter初始用户 期望:alter不报错，但不生效，修改前后不发生改变
    3.无权限用户default018_02连接，for role default018_02 alter sysadmin用户 期望:alter不报错，但不生效，修改前后不发生改变
    4.管理员用户连接清理环境 期望:清理成功
Expect      :
    1.初始用户连接创建用户 default018_01,default018_02 期望:创建成功
    2.无权限用户default018_02连接，for role default018_02 alter初始用户 期望:alter不报错，但不生效，修改前后不发生改变
    3.无权限用户default018_02连接，for role default018_02 alter sysadmin用户 期望:alter不报错，但不生效，修改前后不发生改变
    4.管理员用户连接清理环境 期望:清理成功
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
        logger.info('----------------------1.初始用户连接创建用户 default018_01,default018_02 期望:创建成功--------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        # 初始用户用户名
        self.username = self.userNode.ssh_user
        # 初始用户密码
        self.password = macro.GAUSSDB_INIT_USER_PASSWD

    def test_common_user_permission(self):
        logger.info('------------------------管理员用户连接，创建用户，赋登录权限，建表 期望:创建成功-----------------------------')
        sql_cmd = commonsh.execut_db_sql(f'''
                                        drop owned by default018_01 cascade;
                                        drop owned by default018_02 cascade;
                                        drop role if exists default018_01;
                                        drop role if exists default018_02;
                                        create role default018_01 password '{macro.COMMON_PASSWD}';
                                        create role default018_02 password '{macro.COMMON_PASSWD}';
                                        alter role default018_01 with login;
                                        alter role default018_02 with login;
                                        grant all privileges to default018_01;
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)

        logger.info('-----------------无权限用户default018_02连接，for role default018_02 alter初始用户 期望:alter不报错，但不生效，修改前后不发生改变----------------')
        sql_cmd = "ALTER DEFAULT PRIVILEGES for role default018_02 GRANT ALL PRIVILEGES on tables to "+self.username+" WITH GRANT OPTION ;"\
                  +"ALTER DEFAULT PRIVILEGES for role default018_02 GRANT ALL PRIVILEGES on functions to "+self.username+" WITH GRANT OPTION ;"\
                  +"ALTER DEFAULT PRIVILEGES for role default018_02 GRANT ALL PRIVILEGES on TYPES to "+self.username+" WITH GRANT OPTION ;"
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default018_02 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, msg)
        sql_cmd = "select count(*) from information_schema.table_privileges where grantee='"+self.username+"';"\
                  +"select count(*) from information_schema.usage_privileges where grantee='"+self.username+"';"\
                  +"select count(*) from information_schema.routine_privileges where grantee='"+self.username+"';"
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default018_02 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        result1 = msg
        sql_cmd = "ALTER DEFAULT PRIVILEGES for role default018_02 revoke ALL PRIVILEGES on tables from "+self.username+" cascade constraints;"\
                  +"ALTER DEFAULT PRIVILEGES for role default018_02 revoke ALL PRIVILEGES on functions from "+self.username+" cascade constraints;"\
                  +"ALTER DEFAULT PRIVILEGES for role default018_02 revoke ALL PRIVILEGES on TYPES from "+self.username+" cascade constraints;"
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default018_02 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, msg)
        sql_cmd = "select count(*) from information_schema.table_privileges where grantee='"+self.username+"';"\
                  +"select count(*) from information_schema.usage_privileges where grantee='"+self.username+"';"\
                  +"select count(*) from information_schema.routine_privileges where grantee='"+self.username+"';"
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default018_02 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        result2 = msg
        self.assertEqual(result1, result2)

        logger.info('-----------------无权限用户default018_02连接，for role default018_02 alter初始用户 期望:alter不报错，但不生效，修改前后不发生改变----------------')
        sql_cmd = ( '''
                        ALTER DEFAULT PRIVILEGES for role default018_02 GRANT ALL PRIVILEGES on tables to default018_01 WITH GRANT OPTION ;
                        ALTER DEFAULT PRIVILEGES for role default018_02 GRANT ALL PRIVILEGES on functions to default018_01 WITH GRANT OPTION ;
                        ALTER DEFAULT PRIVILEGES for role default018_02 GRANT ALL PRIVILEGES on TYPES to default018_01 WITH GRANT OPTION ;
                        ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default018_02 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, msg)
        sql_cmd = ( '''
                        select count(*) from information_schema.table_privileges where grantee='default018_01';
                        select count(*) from information_schema.usage_privileges where grantee='default018_01';
                        select count(*) from information_schema.routine_privileges where grantee='default018_01';
                        ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default018_02 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        result1 = msg
        sql_cmd = ( '''
                        ALTER DEFAULT PRIVILEGES for role default018_02 revoke ALL PRIVILEGES on tables from default018_01 cascade constraints;
                        ALTER DEFAULT PRIVILEGES for role default018_02 revoke ALL PRIVILEGES on functions from default018_01 cascade constraints;
                        ALTER DEFAULT PRIVILEGES for role default018_02 revoke ALL PRIVILEGES on TYPES from default018_01 cascade constraints;
                        ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default018_02 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, msg)
        sql_cmd = ( '''
                        select count(*) from information_schema.table_privileges where grantee='default018_01';
                        select count(*) from information_schema.usage_privileges where grantee='default018_01';
                        select count(*) from information_schema.routine_privileges where grantee='default018_01';
                        ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default018_02 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        result2 = msg
        self.assertEqual(result1, result2)

    def tearDown(self):
        logger.info('清理环境')
        sql_cmd = commonsh.execut_db_sql(f'''drop owned by \
            default018_01 cascade;\
            drop owned by default018_02 cascade;\
            drop role if exists default018_01;\
            drop role if exists default018_02;\
                                        ''')
        logger.info(sql_cmd)
        logger.info('Opengauss_Function_Alter_Default_Privileges_Case0018结束')