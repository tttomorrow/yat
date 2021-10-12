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
Case Name   : 测试支持外键约束延迟生效
Description :
    1.创建兼容mysql的数据库 期望:创建成功
    2.建表指定外键关系 期望:创建成功
    3.测试支持外键约束延迟生效 期望:合理报错
    4.创建兼容TD的数据库 期望:创建成功
    5.建表指定外键关系 期望:创建成功
    6.测试支持外键约束延迟生效 期望:合理报错
    7.创建兼容PG的数据库 期望:创建成功
    8.建表指定外键关系 期望:创建成功
    9.测试支持外键约束延迟生效 期望:合理报错
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
            '----------------------------Opengauss_Function_DDL_Parttion_Case0065开始执行-----------------------------')
        self.userNode = Node('dbuser')

        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_Index_file_damaged(self):
        logger.info('----------------------------创建兼容mysql的数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_03 cascade;
                    drop table if exists pteacher_table_03 cascade;
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

        logger.info('--------------------建表指定外键关系 期望:创建成功--------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_03 cascade;
                    drop table if exists pteacher_table_03 cascade;
                    create table pteacher_table_03
                    (
                        t_date timestamp primary key,
                        t_name varchar not null
                    )partition by range(t_date) interval ('10 day') (
                      partition part1 values less than ('1990-02-02 00:00:00'));
                    create table pstudent_table_03
                    (
                        s_date timestamp,
                        s_name varchar not null,
                        t_date timestamp REFERENCES pteacher_table_03 deferrable initially deferred
                    )partition by range(t_date) interval ('10 day') (
                      partition part1 values less than ('1990-02-02 00:00:00'));
                    --添加数据
                    INSERT INTO pteacher_table_03 VALUES (date '2020-09-01', '李老师');
                    INSERT INTO pstudent_table_03 VALUES (date '2020-09-01', '张三', date '2020-09-01');
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

        logger.info('----------------------------测试支持外键约束延迟生效 期望:合理报错-----------------------------')
        sql_cmd = '''
                    START TRANSACTION;
                        INSERT INTO pstudent_table_03 VALUES (date '2020-09-04', '李四', date '2020-09-04');
                        update pstudent_table_03 set s_date = date '2020-09-09';
                    COMMIT;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        logger.info(msg)

        logger.info('----------------------------创建兼容TD的数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_03 cascade;
                    drop table if exists pteacher_table_03 cascade;
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

        logger.info('--------------------建表指定外键关系 期望:创建成功--------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_03 cascade;
                    drop table if exists pteacher_table_03 cascade;
                    create table pteacher_table_03
                    (
                        t_date timestamp primary key,
                        t_name varchar not null
                    )partition by range(t_date) interval ('10 day') (
                      partition part1 values less than ('1990-02-02 00:00:00'));
                    create table pstudent_table_03
                    (
                        s_date timestamp,
                        s_name varchar not null,
                        t_date timestamp REFERENCES pteacher_table_03 deferrable initially deferred
                    )partition by range(t_date) interval ('10 day') (
                      partition part1 values less than ('1990-02-02 00:00:00'));
                    --添加数据
                    INSERT INTO pteacher_table_03 VALUES (date '2020-09-01', '李老师');
                    INSERT INTO pstudent_table_03 VALUES (date '2020-09-01', '张三', date '2020-09-01');
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

        logger.info('----------------------------测试支持外键约束延迟生效 期望:合理报错-----------------------------')
        sql_cmd = '''
                    START TRANSACTION;
                        INSERT INTO pstudent_table_03 VALUES (date '2020-09-04', '李四', date '2020-09-04');
                        update pstudent_table_03 set s_date = date '2020-09-09';
                    COMMIT;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        logger.info(msg)

        logger.info('----------------------------创建兼容PG的数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_03 cascade;
                    drop table if exists pteacher_table_03 cascade;
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

        logger.info('--------------------建表指定外键关系 期望:创建成功--------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_03 cascade;
                    drop table if exists pteacher_table_03 cascade;
                    create table pteacher_table_03
                    (
                        t_date timestamp primary key,
                        t_name varchar not null
                    )partition by range(t_date) interval ('10 day') (
                      partition part1 values less than ('1990-02-02 00:00:00'));
                    create table pstudent_table_03
                    (
                        s_date timestamp,
                        s_name varchar not null,
                        t_date timestamp REFERENCES pteacher_table_03 deferrable initially deferred
                    )partition by range(t_date) interval ('10 day') (
                      partition part1 values less than ('1990-02-02 00:00:00'));
                    --添加数据
                    INSERT INTO pteacher_table_03 VALUES (date '2020-09-01', '李老师');
                    INSERT INTO pstudent_table_03 VALUES (date '2020-09-01', '张三', date '2020-09-01');
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

        logger.info('----------------------------测试支持外键约束延迟生效 期望:合理报错-----------------------------')
        sql_cmd = '''
                    START TRANSACTION;
                        INSERT INTO pstudent_table_03 VALUES (date '2020-09-04', '李四', date '2020-09-04');
                        update pstudent_table_03 set s_date = date '2020-09-09';
                    COMMIT;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        logger.info(msg)

    def tearDown(self):
        logger.info('----------------------------删除表和数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_03 cascade;
                    drop table if exists pteacher_table_03 cascade;
                    drop database if exists pguser;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        logger.info(
            '----------------------------Opengauss_Function_DDL_Parttion_Case0065执行完成-----------------------------')