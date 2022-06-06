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
Case Name   : 测试不支持列存表、内存表建立外键
Description :
    1.创建兼容mysql的数据库 期望:合理报错
    2.建表指定外键关系 期望:合理报错
    3.测试不支持列存表、内存表建立外键 期望:合理报错
    4.创建兼容TD的数据库 期望:合理报错
    5.建表指定外键关系 期望:合理报错
    6.测试不支持列存表、内存表建立外键 期望:合理报错
    7.创建兼容PG的数据库 期望:合理报错
    8.建表指定外键关系 期望:合理报错
    9.测试不支持列存表、内存表建立外键 期望:合理报错
    10.清理环境 期望:清理成功
Expect      :
History     :
"""

import sys
import unittest
from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class IndexFileDamaged(unittest.TestCase):
    def setUp(self):
        logger.info(
            '----------------------------Opengauss_Function_DDL_Parttion_Case0069开始执行-----------------------------')
        self.userNode = Node('dbuser')

        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_Index_file_damaged(self):
        logger.info('----------------------------创建兼容mysql的数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_07;
                    drop table if exists pclass_table_07;
                    drop table if exists pteacher_table_07;
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

        logger.info('--------------------建表指定外键关系 期望:合理报错--------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_07;
                    drop table if exists pclass_table_07;
                    drop table if exists pteacher_table_07;
                    
                    create table pclass_table_07
                    (
                        c_date TIMESTAMP ,
                        c_name varchar not null
                    )with (orientation=column) partition by range(c_date)  (
                      partition part1 values less than ('1990-07-07 00:00:00'));
                    
                    create table pteacher_table_07
                    (
                        t_date TIMESTAMP primary key,
                        t_name varchar not null
                    ) with (orientation=column) partition by range(t_date)  (
                      partition part1 values less than ('1990-07-07 00:00:00'));
                    
                    create table pstudent_table_07
                    (
                        s_date TIMESTAMP,
                        s_name varchar not null,
                        c_date TIMESTAMP,
                        t_date TIMESTAMP,
                        foreign key(c_date) references pclass_table_07(c_date)
                    ) with (orientation=column) partition by range(s_date)  (
                      partition part1 values less than ('1990-07-07 00:00:00'));
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('----------------------------创建兼容TD的数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_07;
                    drop table if exists pclass_table_07;
                    drop table if exists pteacher_table_07;
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
        self.assertIn(self.Constant.DROP_DATABASE_SUCCESS, msg)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, msg)

        logger.info('--------------------建表指定外键关系 期望:合理报错--------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_07;
                    drop table if exists pclass_table_07;
                    drop table if exists pteacher_table_07;

                    create table pclass_table_07
                    (
                        c_date TIMESTAMP ,
                        c_name varchar not null
                    )with (orientation=column) partition by range(c_date)  (
                      partition part1 values less than ('1990-07-07 00:00:00'));

                    create table pteacher_table_07
                    (
                        t_date TIMESTAMP primary key,
                        t_name varchar not null
                    ) with (orientation=column) partition by range(t_date)  (
                      partition part1 values less than ('1990-07-07 00:00:00'));

                    create table pstudent_table_07
                    (
                        s_date TIMESTAMP,
                        s_name varchar not null,
                        c_date TIMESTAMP,
                        t_date TIMESTAMP,
                        foreign key(c_date) references pclass_table_07(c_date)
                    ) with (orientation=column) partition by range(s_date)  (
                      partition part1 values less than ('1990-07-07 00:00:00'));
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('----------------------------创建兼容PG的数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_07;
                    drop table if exists pclass_table_07;
                    drop table if exists pteacher_table_07;
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

        logger.info('--------------------建表指定外键关系 期望:合理报错--------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_07;
                    drop table if exists pclass_table_07;
                    drop table if exists pteacher_table_07;

                    create table pclass_table_07
                    (
                        c_date TIMESTAMP ,
                        c_name varchar not null
                    )with (orientation=column) partition by range(c_date)  (
                      partition part1 values less than ('1990-07-07 00:00:00'));

                    create table pteacher_table_07
                    (
                        t_date TIMESTAMP primary key,
                        t_name varchar not null
                    ) with (orientation=column) partition by range(t_date)  (
                      partition part1 values less than ('1990-07-07 00:00:00'));

                    create table pstudent_table_07
                    (
                        s_date TIMESTAMP,
                        s_name varchar not null,
                        c_date TIMESTAMP,
                        t_date TIMESTAMP,
                        foreign key(c_date) references pclass_table_07(c_date)
                    ) with (orientation=column) partition by range(s_date)  (
                      partition part1 values less than ('1990-07-07 00:00:00'));
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)

    def tearDown(self):
        logger.info('----------------------------删除表和数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_07;
                    drop table if exists pclass_table_07;
                    drop table if exists pteacher_table_07;
                    drop database if exists pguser;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        logger.info('----------------------------Opengauss_Function_DDL_Parttion_Case0069执行完成-----------------------------')