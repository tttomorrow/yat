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
Case Name   : 表（包括视图）进行ALL PRIVILEGES的grant，revoke和drop
Description :
    1.管理员用户连接，创建用户，赋登录权限，建表 期望:创建报错无权限，赋权报错无权限
    2.default004用户连接 执行DML  期望:执行成功
    3.管理员用户连接，执行alter 期望:alter成功，建表建视图成功
    4.default004用户连接 执行DML  期望:执行失败 提示无权限
    5.管理员用户连接，执行alter 期望:alter成功，建表建视图成功
    6.管理员用户连接，执行drop 期望:drop失败
    7.管理员用户连接，执行drop 期望:drop成功
    8.清理环境 drop user 期望:执行成功
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
        logger.info('------------------------Opengauss_Function_Alter_Default_Privileges_Case0004开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_common_user_permission(self):
        logger.info('------------------------管理员用户连接，创建用户，赋登录权限，建表 期望:创建成功-----------------------------')
        sql_cmd = commonsh.execut_db_sql(f'''
                                        drop table if exists test_alter_default_004 cascade;
                                        drop view if exists vim_default004 cascade;
                                        drop user if exists default004 cascade;
                                        create user default004 password '{macro.COMMON_PASSWD}';
                                        ALTER DEFAULT PRIVILEGES  GRANT ALL PRIVILEGES on tables to default004;
                                        create table  test_alter_default_004(id int unique);
                                        create view vim_default004 as select * from test_alter_default_004;
                                        insert into test_alter_default_004 values(1);
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.CREATE_VIEW_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd)

        logger.info('------------------------default004用户连接 执行DML  期望:执行成功-------------------------')
        sql_cmd = ( '''
                        drop table if exists test_alter_default_005 cascade;
                        create table test_alter_default_005(id int unique REFERENCES test_alter_default_004(id)) ;
                        update test_alter_default_004 set id = 101 where id=10101;
                        insert into test_alter_default_004 values(10101);
                        select * from vim_default004;
                        select * from test_alter_default_004;
                        ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default004 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, msg)
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg)
        self.assertIn("row", msg)

        logger.info('------------------------管理员用户连接，执行alter 期望:alter成功，建表成功-----------------------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        ALTER DEFAULT PRIVILEGES  REVOKE ALL PRIVILEGES ON TABLES FROM default004;
                                        drop table if exists test_alter_default_004 cascade;
                                        drop view if exists vim_default004 cascade;
                                        create table  test_alter_default_004(id int unique);
                                        create view vim_default004 as select * from test_alter_default_004;
                                        insert into test_alter_default_004 values(1);
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, sql_cmd)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd)

        logger.info('------------------------default004用户连接 执行DML  期望:执行失败 提示无权限-------------------------')
        sql_cmd = ( '''
                        drop table if exists test_alter_default_005 cascade;
                        create table test_alter_default_005(id int unique REFERENCES test_alter_default_004(id)) ;
                        update test_alter_default_004 set id = 101 where id=10101;
                        insert into test_alter_default_004 values(10101);
                        select * from vim_default004;
                        select * from test_alter_default_004;
                        ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default004 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertNotIn(self.Constant.UPDATE_SUCCESS_MSG, msg)
        self.assertNotIn(self.Constant.INSERT_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg)
        self.assertNotIn("row", msg)

        logger.info('------------------------管理员用户连接，执行alter 期望:alter成功，建表成功-----------------------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        ALTER DEFAULT PRIVILEGES  GRANT ALL PRIVILEGES on tables to default004;
                                        drop table if exists test_alter_default_004 cascade;
                                        drop view if exists vim_default004 cascade;
                                        create table  test_alter_default_004(id int unique);
                                        create view vim_default004 as select * from test_alter_default_004;
                                        insert into test_alter_default_004 values(1);
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, sql_cmd)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd)

        logger.info('----------------------------管理员用户连接，执行drop 期望:drop失败,相关表未删除-----------------------------')
        sql_cmd = ( '''
                        drop user default004;
                        ALTER DEFAULT PRIVILEGES  REVOKE ALL PRIVILEGES ON TABLES FROM default004;
                        ''')
        logger.info(excute_cmd)
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default004 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg.split('row')[0])
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, sql_cmd)

        logger.info('------------------------管理员用户连接，执行drop 期望:drop成功-----------------------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        drop user default004;
                                        DROP OWNED BY default004 cascade;
                                        drop user default004;
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_OWNED_SUCCESS, sql_cmd)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)

    def tearDown(self):
        logger.info('---------------------------------清理环境。期望:删除用户成功-----------------------------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        drop table if exists test_alter_default_004 cascade;
                                        drop table if exists test_alter_default_005 cascade;
                                        ''')
        logger.info(sql_cmd)
        logger.info('-------------------------Opengauss_Function_Alter_Default_Privileges_Case0004执行结束---------------------------')