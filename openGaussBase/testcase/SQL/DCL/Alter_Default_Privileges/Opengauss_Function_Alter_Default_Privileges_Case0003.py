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
Case Name   : 表（包括视图）进行其他权限的revoke
Description :
    1.管理员用户连接，创建用户，赋登录权限，建表 期望:创建报错无权限，赋权报错无权限
    2.default003用户连接 执行DML  期望:REFERENCES成功
    3.管理员用户连接，执行alter 期望:alter成功，建表成功
    4.default003用户连接 执行DML  期望: TRUNCATE成功，REFERENCES报错无权限
    5.管理员用户连接，执行alter 期望:alter成功，建表成功
    6.default003用户连接 执行DML  期望:update成功，truncate报错无权限
    7.管理员用户连接，执行alter  期望:alter成功，建表成功
    8.default003用户连接 执行DML 期望:insert成功，update报错无权限
    9.管理员用户连接，执行alter 期望:alter成功，建表建视图成功
    10.default003用户连接 执行DML 期望:insert报错无权限，select成功
    11.管理员用户连接，执行alter 期望:alter成功，建表建视图成功
    12.default003用户连接，select报错。
    期望:ERROR:  permission denied for relation test_alter_default_003
    期望:ERROR:  permission denied for relation vim_default003
    13.清理环境 期望:删除报错无权限
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
        logger.info('------------Opengauss_Function_Alter_Default_Privileges_Case0003开始执行----------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_common_user_permission(self):
        logger.info('-----------管理员用户连接，创建用户，赋登录权限，建表---------')
        sql_cmd = commonsh.execut_db_sql(f'''
                                        drop table if exists test_alter_default_003 cascade;
                                        drop owned by default003 cascade;
                                        drop user if exists default003 cascade;
                                        create user default003 password '{macro.COMMON_PASSWD}';
                                        ALTER DEFAULT PRIVILEGES grant select,insert,update,truncate,REFERENCES ON TABLES to default003;
                                        create table  test_alter_default_003(id int unique);
                                        insert into test_alter_default_003 values(1);
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd)
        logger.info('------------default003用户连接 执行DML-----------')
        sql_cmd = ( '''
                        drop table if exists test_alter_default_003_02 cascade;
                        create table test_alter_default_003_02(id int unique REFERENCES test_alter_default_003(id)) ;
                        ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default003 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, msg)
        logger.info('--------------管理员用户连接，执行alter----------')
        sql_cmd = commonsh.execut_db_sql('''
                                        ALTER DEFAULT PRIVILEGES REVOKE REFERENCES ON TABLES FROM default003;
                                        drop table if exists test_alter_default_003 cascade;
                                        create table  test_alter_default_003(id int unique);
                                        insert into test_alter_default_003 values(1);
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd)
        logger.info('-----------default003用户连接 执行DML-----------')
        sql_cmd = ( '''
                        truncate test_alter_default_003;
                        select * from test_alter_default_003;
                        drop table if exists test_alter_default_003_02 cascade;
                        create table test_alter_default_003_02(id int unique REFERENCES test_alter_default_003(id)) ;
                        ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default003 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg.split('row')[0])
        self.assertIn(self.Constant.TRUNCATE_SUCCESS_MSG, msg.split('row')[0])
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg.split('row')[-1])
        self.assertIn(self.Constant.PERMISSION_DENIED, msg.split('row')[-1])
        logger.info('--------管理员用户连接，执行alter-----------')
        sql_cmd = commonsh.execut_db_sql('''
                                        ALTER DEFAULT PRIVILEGES REVOKE truncate ON TABLES FROM default003;
                                        drop table if exists test_alter_default_003 cascade;
                                        create table  test_alter_default_003(id int unique);
                                        insert into test_alter_default_003 values(10101);
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        logger.info('----------default003用户连接 执行DML----------')
        sql_cmd = ( '''
                        update test_alter_default_003 set id = 101 where id=10101;
                        select * from test_alter_default_003;
                        truncate test_alter_default_003;
                        ''')
        logger.info(excute_cmd)
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default003 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg.split('row')[0])
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, msg.split('row')[0])
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg.split('row')[-1])
        self.assertIn(self.Constant.PERMISSION_DENIED, msg.split('row')[-1])
        logger.info('----------管理员用户连接，执行alter-------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        ALTER DEFAULT PRIVILEGES GRANT update ON TABLES TO default003;
                                        drop table if exists test_alter_default_003 cascade;
                                        create table  test_alter_default_003(id int);
                                        insert into test_alter_default_003 values(10101);
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        logger.info('----------default003用户连接 执行DML------------')
        sql_cmd = ( '''
                        update test_alter_default_003 set id = 101 where id=10101;
                        select * from test_alter_default_003;
                        truncate test_alter_default_003;
                        ''')
        logger.info(excute_cmd)
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default003 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg.split('row')[0])
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, msg.split('row')[0])
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg.split('row')[-1])
        self.assertIn(self.Constant.PERMISSION_DENIED, msg.split('row')[-1])
        logger.info('----------管理员用户连接，执行alter------------')
        sql_cmd = commonsh.execut_db_sql('''
                                        ALTER DEFAULT PRIVILEGES REVOKE update ON TABLES FROM default003;
                                        drop table if exists test_alter_default_003 cascade;
                                        create table  test_alter_default_003(id int);
                                        insert into test_alter_default_003 values(10101);
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        logger.info('---------default003用户连接 执行DML----------')
        sql_cmd = ('''
                    insert into test_alter_default_003 values(10101);
                    select * from test_alter_default_003;
                    update test_alter_default_003 set id = 101 where id=10101;
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default003 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg)
        logger.info('------------管理员用户连接，执行alter-----------')
        sql_cmd = commonsh.execut_db_sql('''
                                        ALTER DEFAULT PRIVILEGES REVOKE insert ON TABLES FROM default003;
                                        drop table if exists test_alter_default_003 cascade;
                                        drop view if exists vim_default003 cascade;
                                        create table  test_alter_default_003(id int);
                                        create view vim_default003 as select * from test_alter_default_003;
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        logger.info('-----------default003用户连接 执行DML------------')
        sql_cmd = ( '''
                    select * from test_alter_default_003,vim_default003;
                    insert into test_alter_default_003 values(10101);
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default003 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg.split('row')[0])
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg.split('row')[-1])
        self.assertIn(self.Constant.PERMISSION_DENIED, msg.split('row')[-1])
        logger.info('---------管理员用户连接，执行alter----------')
        sql_cmd = commonsh.execut_db_sql('''
                                        ALTER DEFAULT PRIVILEGES REVOKE SELECT ON TABLES FROM default003;
                                        drop table if exists test_alter_default_003 cascade;
                                        drop view if exists vim_default003 cascade;
                                        create table  test_alter_default_003(id int);
                                        create view vim_default003 as select * from test_alter_default_003;
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DEFAULT_PRIVILEGES, sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        logger.info('-----------default003用户连接 期望:ERROR:  permission denied for relation test_alter_default_003-------------')
        sql_cmd = ( '''
                    select * from test_alter_default_003;
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U default003 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg)
    def tearDown(self):
        logger.info('---------------清理环境---------------')
        sql_cmd = commonsh.execut_db_sql('''
            drop table if exists test_alter_default_003 cascade;
            drop owned by default003 cascade;
            drop user if exists default003 cascade;''')
        logger.info(sql_cmd)
        logger.info('-----------Opengauss_Function_Alter_Default_Privileges_Case0003执行结束------------')