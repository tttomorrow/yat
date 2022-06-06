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
Case Name   : 测试A表主键多个字段对应B表多个字段主键
Description :
    1.创建兼容TD的数据库 期望:创建成功
    2.建表指定外键关系 期望:创建成功
    3.检测A表主键对应B表多个外键 期望:操作成功
    4.创建兼容PG的数据库 期望:创建成功
    5.建表指定外键关系 期望:创建成功
    6.检测A表主键对应B表多个外键 期望:操作成功
    7.清理环境 期望:清理成功
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
            '----------------------------Opengauss_Function_DDL_Parttion_Case0068开始执行-----------------------------')
        self.userNode = Node('dbuser')

        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_Index_file_damaged(self):
        logger.info('----------------------------创建兼容TD的数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pteacher_table_06 cascade;
                    drop table if exists pstudent_table_06 cascade;
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
                    drop table if exists pteacher_table_06 cascade;
                    drop table if exists pstudent_table_06 cascade;
                    create table pteacher_table_06
                    (
                        t_date timestamp,
                        t_day timestamp,
                        t_name varchar not null,
                        primary key (t_date, t_day)
                    )partition by range(t_date) interval ('10 day') (partition part1 values less than ('1990-02-02 00:00:00'));
                    create table pstudent_table_06
                    (
                        s_date timestamp primary key,
                        s_name varchar not null,
                        t_date timestamp,
                        t_day timestamp,
                        CONSTRAINT FK_pstudent_table_06_1 FOREIGN KEY (t_date, t_day) REFERENCES pteacher_table_06 on update cascade on delete set null
                    )partition by range(s_date) interval ('10 day') (partition part1 values less than ('1990-02-02 00:00:00'));
                    
                    insert into pteacher_table_06 values (date '2020-09-01', date '2020-09-01', '张老师');
                    insert into pteacher_table_06 values (date '2020-09-02', date '2020-09-02', '李老师');
                    insert into pteacher_table_06 values (date '2020-09-03', date '2020-09-03', '陈老师');
                    
                    insert into pstudent_table_06 values (date '2020-09-01', '王二', date '2020-09-01', date '2020-09-01');
                    insert into pstudent_table_06 values (date '2020-09-02', '张三', date '2020-09-02', date '2020-09-02');
                    insert into pstudent_table_06 values (date '2020-09-03', '吴五', date '2020-09-03', null);
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
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, msg)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

        logger.info('----------------------------测试A表主键多个字段对应B表多个字段主键 期望:合理报错-----------------------------')
        sql_cmd = '''
                    delete from pstudent_table_06 where s_date = date '2020-09-03';
                    alter table pstudent_table_06 drop constraint FK_pstudent_table_06_1;
                    alter table pstudent_table_06 add constraint FK_pstudent_table_06_2 FOREIGN KEY (t_date, t_day) REFERENCES pteacher_table_06 MATCH FULL on update cascade on delete set null;

                    insert into pstudent_table_06 values (date '2020-09-04', '陈一', date '2020-09-02', date '2020-09-03');
                    insert into pstudent_table_06 values (date '2020-09-05', '李四', date '2020-09-03', null);
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.ALTER_TABLE_MSG, msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        logger.info(msg)
        logger.info('----------------------------测试update和delete情况 期望:操作成功-----------------------------')
        sql_cmd = '''
                    select * from pstudent_table_06;
                    update pteacher_table_06 set t_date = date '2020-09-09' where t_date = date '2020-09-01';
                    select * from pstudent_table_06;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, msg)
        self.assertIn("2020-09-09", msg)
        logger.info(msg)
        sql_cmd = '''
                    delete from pteacher_table_06 where t_day = date '2020-09-01';
                    select * from pstudent_table_06;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.DELETE_SUCCESS_MSG, msg)
        self.assertNotIn("2020-09-09", msg)
        logger.info(msg)


        logger.info('----------------------------创建兼容PG的数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pteacher_table_06 cascade;
                    drop table if exists pstudent_table_06 cascade;
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
                    drop table if exists pteacher_table_06 cascade;
                    drop table if exists pstudent_table_06 cascade;
                    create table pteacher_table_06
                    (
                        t_date timestamp,
                        t_day timestamp,
                        t_name varchar not null,
                        primary key (t_date, t_day)
                    )partition by range(t_date) interval ('10 day') (partition part1 values less than ('1990-02-02 00:00:00'));
                    create table pstudent_table_06
                    (
                        s_date timestamp primary key,
                        s_name varchar not null,
                        t_date timestamp,
                        t_day timestamp,
                        CONSTRAINT FK_pstudent_table_06_1 FOREIGN KEY (t_date, t_day) REFERENCES pteacher_table_06 on update cascade on delete set null
                    )partition by range(s_date) interval ('10 day') (partition part1 values less than ('1990-02-02 00:00:00'));

                    insert into pteacher_table_06 values (date '2020-09-01', date '2020-09-01', '张老师');
                    insert into pteacher_table_06 values (date '2020-09-02', date '2020-09-02', '李老师');
                    insert into pteacher_table_06 values (date '2020-09-03', date '2020-09-03', '陈老师');

                    insert into pstudent_table_06 values (date '2020-09-01', '王二', date '2020-09-01', date '2020-09-01');
                    insert into pstudent_table_06 values (date '2020-09-02', '张三', date '2020-09-02', date '2020-09-02');
                    insert into pstudent_table_06 values (date '2020-09-03', '吴五', date '2020-09-03', null);
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
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('----------------------------测试A表主键多个字段对应B表多个字段主键 期望:合理报错-----------------------------')
        sql_cmd = '''
                    delete from pstudent_table_06 where s_date = date '2020-09-03';
                    alter table pstudent_table_06 drop constraint FK_pstudent_table_06_1;
                    alter table pstudent_table_06 add constraint FK_pstudent_table_06_2 FOREIGN KEY (t_date, t_day) REFERENCES pteacher_table_06 MATCH FULL on update cascade on delete set null;

                    insert into pstudent_table_06 values (date '2020-09-04', '陈一', date '2020-09-02', date '2020-09-03');
                    insert into pstudent_table_06 values (date '2020-09-05', '李四', date '2020-09-03', null);
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.ALTER_TABLE_MSG, msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        logger.info(msg)
        logger.info('----------------------------测试update和delete情况 期望:操作成功-----------------------------')
        sql_cmd = '''
                    select * from pstudent_table_06;
                    update pteacher_table_06 set t_date = date '2020-09-09' where t_date = date '2020-09-01';
                    select * from pstudent_table_06;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, msg)
        self.assertIn("2020-09-09", msg)
        logger.info(msg)
        sql_cmd = '''
                    delete from pteacher_table_06 where t_day = date '2020-09-01';
                    select * from pstudent_table_06;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.DELETE_SUCCESS_MSG, msg)
        self.assertNotIn("2020-09-09", msg)
        logger.info(msg)

    def tearDown(self):
        logger.info('----------------------------删除表和数据库-----------------------------')
        sql_cmd = '''
                    drop table if exists pteacher_table_06 cascade;
                    drop table if exists pstudent_table_06 cascade;
                    drop database if exists pguser;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        logger.info('----------------------------Opengauss_Function_DDL_Parttion_Case0068执行完成-----------------------------')