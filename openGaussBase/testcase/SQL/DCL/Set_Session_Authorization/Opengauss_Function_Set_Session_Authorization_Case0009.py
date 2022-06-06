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
Case Name   : RESET SESSION AUTHORIZATION
Description :
    1.使用初始用户连gsql，创建用户，给用户赋登录权限，期望:创建赋权成功
    2.使用role9_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role9_001
    3.使用role9_001连接gsql，执行set role语句设置为group用户role9_002 期望:设置成功，查询SESSION_USER和CURRENT_USER为role9_002
    4.使用role9_001连接gsql，执行RESET SESSION AUTHORIZATION 期望:resset成功，查询SESSION_USER和CURRENT_USER为role9_001
    5.使用初始用户连gsql，删除表 期望:删除成功
    6.使用role9_001连接gsql,执行RESET SESSION AUTHORIZATION 期望:resset成功，查询table_set_role9_001属主为role9_002 table_set_role9_002属主为role9_001，查询SESSION_USER和CURRENT_USER为role9_001
    7.使用初始用户连gsql，清理环境。期望:删除用户成功
Expect      :
History     :
"""



import sys
import unittest
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_Set_Session_Authorization_Case0009开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_common_user_permission(self):
        logger.info('------------------------创建用户，给用户赋权为sysadmin，期望:创建赋权成功-----------------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''
                                            drop table if exists table_set_role9_001 cascade;
                                            drop table if exists table_set_role9_002 cascade;
                                            drop owned by role9_001 cascade;
                                            drop owned by role9_002 cascade;
                                            drop role if exists role9_001;
                                            drop role if exists role9_002;
                                            create role role9_001  password '{macro.COMMON_PASSWD}';
                                            create role role9_002  password '{macro.COMMON_PASSWD}';
                                            alter role role9_001 with login;
                                            alter role role9_002 with login;
                                            grant all privileges to role9_001;
                                            grant all privileges to role9_002;
                                            ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)

        logger.info('-----------使用role9_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role9_001-------------')
        sql_cmd = ('''
                    SELECT SESSION_USER, CURRENT_USER;
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role9_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("role9_001", msg)

        logger.info('----------使用role9_001连接gsql，执行set role语句设置为role9_002 期望:设置成功，查询均为role9_002---------')
        logger.info('----------执行RESET SESSION AUTHORIZATION 期望:resset成功，查询CURRENT_USER为role9_001---------')
        sql_cmd = (f'''
                    SET SESSION AUTHORIZATION role9_002 password '{macro.COMMON_PASSWD}';
                    SELECT SESSION_USER, CURRENT_USER;
                    RESET SESSION AUTHORIZATION;
                    SELECT SESSION_USER, CURRENT_USER;
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role9_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("SET", msg)
        self.assertIn("RESET", msg)
        self.assertIn("role9_001", msg)
        self.assertIn("role9_002", msg)

        logger.info('------------------------使用初始用户连gsql，删除表 期望:删除成功-----------------------------')
        sql_cmd = self.commonsh.execut_db_sql('''
                                            drop table if exists table_set_role9_001 cascade;
                                            drop table if exists table_set_role9_002 cascade;
                                            ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, sql_cmd)

        logger.info('----------使用role9_001连接gsql,执行RESET SESSION AUTHORIZATION 期望:resset成功，查询table_set_role9_001属主为role9_002 table_set_role9_002属主为role9_001，查询CURRENT_USER为role9_001---------')
        sql_cmd = (f'''
                    START TRANSACTION;
                        SET local SESSION AUTHORIZATION role9_002 password '{macro.COMMON_PASSWD}';
                        create table table_set_role9_001(id int);
                        RESET SESSION AUTHORIZATION;
                        create table table_set_role9_002(id int);
                    end;
                    SELECT SESSION_USER, CURRENT_USER;
                    select tableowner from pg_tables where tablename ='table_set_role9_002';
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role9_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("role9_001", msg)
        self.assertNotIn("role9_002", msg)

        logger.info('------------------------查询table_set_role9_001属主为role9_002-----------------------------')
        sql_cmd = self.commonsh.execut_db_sql('''
                                            select tableowner from pg_tables where tablename ='table_set_role9_001';
                                            ''')
        logger.info(sql_cmd)
        self.assertIn("role9_002", sql_cmd)
        self.assertNotIn("role9_001", sql_cmd)

    def tearDown(self):
        logger.info('---------------------------------清理环境。期望:删除表和用户成功-----------------------------------')
        sql_cmd = self.commonsh.execut_db_sql('''
                                        drop table if exists table_set_role9_001 cascade;
                                        drop table if exists table_set_role9_002 cascade;
                                        drop owned by role9_001 cascade;
                                        drop owned by role9_002 cascade;
                                        drop role if exists role9_001;
                                        drop role if exists role9_002;
                                        ''')
        logger.info(sql_cmd)
        logger.info('-------------------------Opengauss_Function_Set_Session_Authorization_Case0009执行结束---------------------------')
