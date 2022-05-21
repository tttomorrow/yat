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
Case Name   : 检测是否支持表中建立、更新、删除外键 行存 列存 内存表:success
Description :
    1.创建兼容mysql的数据库 期望:创建成功
    2.建表指定外键关系 期望:创建成功
    3.外键的更新和删除 期望:修改成功
    4.创建兼容TD的数据库 期望:创建成功
    5.建表指定外键关系 期望:创建成功
    6.外键的更新和删除 期望:修改成功
    7.创建兼容PG的数据库 期望:创建成功
    8.建表指定外键关系 期望:创建成功
    9.外键的更新和删除 期望:修改成功
    10.清理环境 期望:清理成功
Expect      :
History     :
"""

import sys
import unittest
from yat.test import Node
from yat.test import macro
sys.path.append(sys.path[0]+"/../")
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
logger = Logger()


class IndexFileDamaged(unittest.TestCase):
    def setUp(self):
        logger.info(
            '----------------------------Opengauss_Function_DDL_Parttion_Case0063开始执行-----------------------------')
        self.userNode = Node('dbuser')

        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_Index_file_damaged(self):
        logger.info('----------------------------创建兼容mysql的数据库-----------------------------')
        sql_cmd = '''
                    drop table pclass_table_01 cascade;
                    drop table pteacher_table_01 cascade;
                    drop table pstudent_table_01 cascade;
                    drop database if exists pguser;
                    CREATE DATABASE pguser DBCOMPATIBILITY 'B';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.DROP_DATABASE_SUCCESS, msg)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, msg)

        logger.info('----------------------------建表-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_01 cascade;
                    drop table if exists pclass_table_01 cascade;
                    drop table if exists pteacher_table_01 cascade;
                    create table pclass_table_01
                    (
                        c_date TIMESTAMP primary key,
                        c_name varchar not null
                    )partition by range(c_date) interval ('10 day') (
                      partition part1 values less than ('1990-01-01 00:00:00'));
                    
                    
                    create table pteacher_table_01
                    (
                        t_date TIMESTAMP primary key,
                        t_name varchar not null
                    )partition by range(t_date) interval ('10 day') (
                      partition part1 values less than ('1990-01-01 00:00:00'));
                    
                    create table pstudent_table_01
                    (
                        s_date TIMESTAMP primary key,
                        s_name varchar not null,
                        c_date TIMESTAMP,
                        t_date TIMESTAMP,
                        foreign key(c_date) references pclass_table_01(c_date)
                    )partition by range(s_date) interval ('10 day') (
                      partition part1 values less than ('1990-01-01 00:00:00'));
                        '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, msg)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

        logger.info('----------------------------外键更新的更新和删除-----------------------------')
        sql_cmd = '''
                    alter table pstudent_table_01 add constraint fk_student_tid foreign key (t_date) references pteacher_table_01(t_date);
                    alter table pstudent_table_01 drop constraint fk_student_tid;
                    alter table pstudent_table_01 drop constraint pstudent_table_01_c_date_fkey;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.ALTER_TABLE_MSG, msg)
        logger.info(msg)

        logger.info('----------------------------创建兼容TD的数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pclass_table_01 cascade;
                    drop table if exists pteacher_table_01 cascade;
                    drop table if exists pstudent_table_01 cascade;
                    drop database if exists pguser;
                    CREATE DATABASE pguser DBCOMPATIBILITY 'C';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, msg)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, msg)

        logger.info('----------------------------建表-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_01 cascade;
                    drop table if exists pclass_table_01 cascade;
                    drop table if exists pteacher_table_01 cascade;
                    create table pclass_table_01
                    (
                        c_date TIMESTAMP primary key,
                        c_name varchar not null
                    )partition by range(c_date) interval ('10 day') (
                      partition part1 values less than ('1990-01-01 00:00:00'));
        
        
                    create table pteacher_table_01
                    (
                        t_date TIMESTAMP primary key,
                        t_name varchar not null
                    )partition by range(t_date) interval ('10 day') (
                      partition part1 values less than ('1990-01-01 00:00:00'));
        
                    create table pstudent_table_01
                    (
                        s_date TIMESTAMP primary key,
                        s_name varchar not null,
                        c_date TIMESTAMP,
                        t_date TIMESTAMP,
                        foreign key(c_date) references pclass_table_01(c_date)
                    )partition by range(s_date) interval ('10 day') (
                      partition part1 values less than ('1990-01-01 00:00:00'));
                        '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, msg)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

        logger.info('----------------------------外键更新的更新和删除-----------------------------')
        sql_cmd = '''
                    alter table pstudent_table_01 add constraint fk_student_tid foreign key (t_date) references pteacher_table_01(t_date);
                    alter table pstudent_table_01 drop constraint fk_student_tid;
                    alter table pstudent_table_01 drop constraint pstudent_table_01_c_date_fkey;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.ALTER_TABLE_MSG, msg)
        logger.info(msg)

        logger.info('----------------------------创建兼容PG的数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pclass_table_01 cascade;
                    drop table if exists pteacher_table_01 cascade;
                    drop table if exists pstudent_table_01 cascade;
                    drop database if exists pguser;
                    CREATE DATABASE pguser DBCOMPATIBILITY 'PG';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.DROP_DATABASE_SUCCESS, msg)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, msg)

        logger.info('----------------------------建表-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_01 cascade;
                    drop table if exists pclass_table_01 cascade;
                    drop table if exists pteacher_table_01 cascade;
                    create table pclass_table_01
                    (
                        c_date TIMESTAMP primary key,
                        c_name varchar not null
                    )partition by range(c_date) interval ('10 day') (
                      partition part1 values less than ('1990-01-01 00:00:00'));
        
        
                    create table pteacher_table_01
                    (
                        t_date TIMESTAMP primary key,
                        t_name varchar not null
                    )partition by range(t_date) interval ('10 day') (
                      partition part1 values less than ('1990-01-01 00:00:00'));
        
                    create table pstudent_table_01
                    (
                        s_date TIMESTAMP primary key,
                        s_name varchar not null,
                        c_date TIMESTAMP,
                        t_date TIMESTAMP,
                        foreign key(c_date) references pclass_table_01(c_date)
                    )partition by range(s_date) interval ('10 day') (
                      partition part1 values less than ('1990-01-01 00:00:00'));
                        '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, msg)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

        logger.info('----------------------------外键更新的更新和删除-----------------------------')
        sql_cmd = '''
                    alter table pstudent_table_01 add constraint fk_student_tid foreign key (t_date) references pteacher_table_01(t_date);
                    alter table pstudent_table_01 drop constraint fk_student_tid;
                    alter table pstudent_table_01 drop constraint pstudent_table_01_c_date_fkey;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.ALTER_TABLE_MSG, msg)
        logger.info(msg)

    def tearDown(self):
        logger.info('----------------------------删除表和数据库-----------------------------')
        sql_cmd = '''
                    drop table pclass_table_01 cascade;
                    drop table pteacher_table_01 cascade;
                    drop table pstudent_table_01 cascade;
                    drop database if exists pguser;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        logger.info('----------------------------Opengauss_Function_DDL_Parttion_Case0063执行完成-----------------------------')