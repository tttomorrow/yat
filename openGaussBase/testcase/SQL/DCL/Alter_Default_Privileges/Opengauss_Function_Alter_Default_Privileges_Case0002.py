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
Case Type   : SQL_DCL
Case Name   : 在表和视图上对用户进行ALL PRIVILEGES的alter
Description :
    1.初始用户连接，创建用户，赋登录权限，建表
    2.default002用户连接 执行DML
    3.初始用户连接，执行alter
    4.default002用户连接 执行DML
    5.初始用户连接，执行alter
    6.default002用户连接 执行DML
    7.恢复环境
Expect      :
    1.初始用户连接，创建用户，赋登录权限，建表成功
    2.default002用户连接 执行DML  期望:执行失败
    3.初始用户连接，执行alter 期望:alter成功，建表成功
    4.default002用户连接 执行DML  期望:执行成功
    5.初始用户连接，执行alter 期望:alter成功，建表成功
    6.default002用户连接 执行DML  期望:执行失败
    7.恢复环境
History     : 
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_Alter_Default_Privileges_Case0002开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_server_tools1(self):
        self.log.info('--步骤1.初始用户连接，创建用户，赋登录权限，建表--')
        sql_cmd = f'''
            drop owned by default002 cascade;
            drop user if exists default002 cascade;
            drop table if exists test_alter_default_002 cascade;
            create user default002 password '{macro.PASSWD_REPLACE}';
            alter user default002 with login;
            create table  test_alter_default_002(id int unique);
            insert into test_alter_default_002 values(1);
            drop view if exists vim_default002;
            create view vim_default002 as select * from \
            test_alter_default_002;
            '''
        sql_result = self.commonsh.execut_db_sql(sql=sql_cmd,
                                                 sql_type=f'-U '
                                                 f'{self.dbuser.ssh_user} '
                                                 f'-W {macro.PASSWD_REPLACE}')
        self.log.info(sql_result)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_result)
        self.assertIn(self.Constant.CREATE_VIEW_SUCCESS_MSG, sql_result)

        self.log.info('--步骤2.default002用户连接 执行DML  期望:执行失败--')
        sql_cmd = f'''
            select * from test_alter_default_002;
            insert into test_alter_default_002 values(2);
            update test_alter_default_002 set  id = 3 where id = 2;
            comment on column test_alter_default_002.id is 'test comment';
            delete from test_alter_default_002 where id = 1;
            truncate test_alter_default_002;
            drop table if exists test_alter_default_003 cascade;
            create table test_alter_default_003(id int unique \
            references test_alter_default_002(id)) ;
            alter table test_alter_default_002 add (c_int int);
            drop index if exists test_index_default002;
            create index test_index_default002 on test_alter_default_002(id);
            vacuum test_alter_default_002;
            drop table test_alter_default_002 cascade;
            '''
        sql_result = self.commonsh.execut_db_sql(sql=sql_cmd,
                                                 sql_type=f'-U default002 '
                                                 f'-W {macro.PASSWD_REPLACE}')
        self.log.info(sql_result)
        self.assertIn(
            'ERROR:  permission denied for relation test_alter_default_002',
            sql_result)

        self.log.info('--步骤3.初始用户连接，执行alter 期望:alter成功，建表成功--')
        sql_cmd = f'''
            grant create on schema public to default002;
            alter default privileges in schema public grant \
            all privileges on tables to default002;
            drop table if exists test_alter_default_002 cascade;
            create table  test_alter_default_002(id int unique);
            insert into test_alter_default_002 values(1);
            drop view if exists vim_default002;
            create view vim_default002 as select * \
            from test_alter_default_002;
            '''
        sql_result = self.commonsh.execut_db_sql(sql=sql_cmd,
                                                 sql_type=f'-U '
                                                 f'{self.dbuser.ssh_user} '
                                                 f'-W {macro.PASSWD_REPLACE}')
        self.log.info(sql_result)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, sql_result)
        self.assertIn(self.Constant.CREATE_VIEW_SUCCESS_MSG, sql_result)

        self.log.info('--步骤4.default002用户连接 执行DML  期望:执行成功--')
        sql_cmd = f'''
            select * from test_alter_default_002;
            insert into test_alter_default_002 values(2);
            update test_alter_default_002 set  id = 3 where id = 2;
            comment on column test_alter_default_002.id is 'test comment';
            delete from test_alter_default_002 where id = 1;
            truncate test_alter_default_002;
            drop table if exists test_alter_default_003 cascade;
            create table test_alter_default_003(id int unique \
            references test_alter_default_002(id)) ;
            alter table test_alter_default_002 add (c_int int);
            drop index if exists test_index_default002;
            create index test_index_default002 on test_alter_default_002(id);
            vacuum test_alter_default_002;
            drop table test_alter_default_002 cascade;
            '''
        sql_result = self.commonsh.execut_db_sql(sql=sql_cmd,
                                                 sql_type=f'-U '
                                                 f'default002 '
                                                 f'-W {macro.PASSWD_REPLACE}')
        self.log.info(sql_result)
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS, sql_result)
        self.assertIn(self.Constant.VACUUM_SUCCESS_MSG, sql_result)

        self.log.info('--步骤5.初始用户连接，执行alter 期望:alter成功，建表成功--')
        sql_cmd = f'''
            grant create on schema public to default002;
            alter default privileges in schema public revoke all \
            privileges on tables from default002;
            drop table if exists test_alter_default_002 cascade;
            create table  test_alter_default_002(id int unique);
            insert into test_alter_default_002 values(1);
            drop view if exists vim_default002;
            create view vim_default002 as select * from \
            test_alter_default_002;
            '''
        sql_result = self.commonsh.execut_db_sql(sql=sql_cmd,
                                                 sql_type=f'-U '
                                                 f'{self.dbuser.ssh_user} '
                                                 f'-W {macro.PASSWD_REPLACE}')
        self.log.info(sql_result)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, sql_result)
        self.assertIn(self.Constant.CREATE_VIEW_SUCCESS_MSG, sql_result)

        self.log.info('--步骤6.default002用户连接 执行DML  期望:执行失败--')
        sql_cmd = f'''
            select * from test_alter_default_002;
            insert into test_alter_default_002 values(2);
            update test_alter_default_002 set  id = 3 where id = 2;
            comment on column test_alter_default_002.id is 'test comment';
            delete from test_alter_default_002 where id = 1;
            truncate test_alter_default_002;
            drop table if exists test_alter_default_003 cascade;
            create table test_alter_default_003(id int unique \
            references test_alter_default_002(id)) ;
            alter table test_alter_default_002 add (c_int int);
            drop index if exists test_index_default002;
            create index test_index_default002 on test_alter_default_002(id);
            vacuum test_alter_default_002;
            drop table test_alter_default_002 cascade;
            '''
        sql_result = self.commonsh.execut_db_sql(sql=sql_cmd,
                                                 sql_type=f'-U '
                                                 f'default002 '
                                                 f'-W {macro.PASSWD_REPLACE}')
        self.log.info(sql_result)
        self.assertIn(
            'ERROR:  permission denied for relation test_alter_default_002',
            sql_result)

    def tearDown(self):
        self.log.info("-----步骤7.恢复环境-------")
        sql_cmd = self.commonsh.execut_db_sql(f'''
            drop table if exists test_alter_default_002 cascade;
            drop table if exists test_alter_default_003 cascade;
            drop view if exists vim_default002 cascade;
            drop owned by default002 cascade;
            drop user if exists default002 cascade;
            ''')
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_Alter_Default_Privileges_Case0002结束')
