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
Case Name   : 检测是否支持不同约束等级下的外键操作:合理报错
Description :
    1.创建兼容mysql的数据库 期望:创建成功
    2.建表指定主键关系 插入数据 期望:创建成功，插入数据成功
    3.增加外键约束 期望:增加成功
    4.测试不同约束等级下的外键操作 期望:操作成功
    5.更新外键 期望:更新成功
    6.测试不同约束等级下的外键操作 期望:操作成功
    7.删除表 期望:删除成功
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
            '----------------------------Opengauss_Function_DDL_Parttion_Case0064开始执行-----------------------------')
        self.userNode = Node('dbuser')

        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_Index_file_damaged(self):
        logger.info('----------------------------创建兼容mysql的数据库 期望:创建成功-----------------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_02 cascade;
                    drop table if exists pclass_table_02 cascade;
                    drop table if exists pteacher_table_02 cascade;
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

        logger.info('----------------------建表指定主键关系 插入数据 期望:创建成功，插入数据成功---------------------')
        sql_cmd = '''
                    drop table if exists pstudent_table_02 cascade;
                    drop table if exists pclass_table_02 cascade;
                    drop table if exists pteacher_table_02 cascade;
                    
                    create table pclass_table_02
                    (
                        c_date TIMESTAMP primary key,
                        c_name varchar not null
                    )partition by range(c_date) interval ('10 day') (
                      partition part1 values less than ('1990-02-02 00:00:00'));
                    
                    
                    create table pteacher_table_02
                    (
                        t_date TIMESTAMP primary key,
                        t_name varchar not null
                    )partition by range(t_date) interval ('10 day') (
                      partition part1 values less than ('1990-02-02 00:00:00'));
                    
                    create table pstudent_table_02
                    (
                        s_date TIMESTAMP primary key,
                        s_name varchar not null,
                        c_date TIMESTAMP,
                        t_date TIMESTAMP,
                        foreign key(c_date) references pclass_table_02(c_date)
                    )partition by range(s_date) interval ('10 day') (
                      partition part1 values less than ('1990-02-02 00:00:00'));
                    
                    --添加数据
                    insert into pclass_table_02 values (date '2020-09-01', '1年1班');
                    insert into pclass_table_02 values (date '2020-09-02', '1年2班');
                    insert into pclass_table_02 values (date '2020-09-03', '1年3班');
                    insert into pclass_table_02 values (date '2020-09-04', '1年4班');
                    insert into pteacher_table_02 values (date '2020-09-01', '李老师');
                    insert into pteacher_table_02 values (date '2020-09-02', '张老师');
                    insert into pteacher_table_02 values (date '2020-09-03', '陈老师');
                    insert into pteacher_table_02 values (date '2020-09-04', '杨老师');
                    insert into pstudent_table_02 values (date '2020-09-01', '张三', date '2020-09-01', date '2020-09-01');
                    insert into pstudent_table_02 values (date '2020-09-02', '李四', date '2020-09-02', date '2020-09-02');
                    insert into pstudent_table_02 values (date '2020-09-03', '王二', date '2020-09-03', date '2020-09-03');
                    insert into pstudent_table_02 values (date '2020-09-04', '李明', date '2020-09-04', date '2020-09-04');
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
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('----------------------------增加外键约束 期望:增加成功-----------------------------')
        sql_cmd = '''
                    alter table pstudent_table_02 add constraint fk_student_tid foreign key (t_date)
                    references pteacher_table_02(t_date) on delete set null on update no action;
                    
                    alter table pstudent_table_02 add constraint fk_student_cid foreign key (c_date)
                    references pclass_table_02(c_date) on delete cascade on update restrict;
                    
                    select conname, convalidated, confupdtype, confdeltype, confmatchtype
                    from PG_CONSTRAINT where conname in ('fk_student_tid', 'fk_student_cid');
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.ALTER_TABLE_MSG, msg)
        logger.info(msg)

        logger.info('----------------------------测试不同约束等级下的外键操作 期望:操作成功-----------------------------')
        sql_cmd = '''
                    delete from pteacher_table_02 where t_date = date '2020-09-04';
                    select t_date from pstudent_table_02 where s_name='李明';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.DELETE_SUCCESS_MSG, msg)
        self.assertEqual(msg.split('\n')[-2],' ')
        logger.info(msg)

        sql_cmd = '''             
                    delete from pclass_table_02 where c_date = date '2020-09-04';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn("violates foreign key constraint", msg)
        logger.info(msg)

        sql_cmd = '''
                    update pteacher_table_02 set t_date = date '2020-09-09' where t_date = date '2020-09-03';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn("violates foreign key constraint", msg)
        logger.info(msg)

        sql_cmd = '''
                    update pclass_table_02 set c_date = date '2020-09-09' where c_date = date '2020-09-04';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn("violates foreign key constraint", msg)
        logger.info(msg)

        logger.info('----------------------------更新外键 期望:更新成功-----------------------------')
        sql_cmd = '''
                    alter table pstudent_table_02 drop constraint fk_student_cid;
                    alter table pstudent_table_02 drop constraint fk_student_tid;
                    alter table pstudent_table_02 add constraint fk_pstudent_table_02_tdate foreign key (t_date) references pteacher_table_02(t_date) on delete no action on update cascade;
                    alter table pstudent_table_02 add constraint fk_pstudent_table_02_cdate foreign key (c_date) references pclass_table_02(c_date) on delete restrict on update set null;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.ALTER_TABLE_MSG, msg)
        logger.info(msg)


        logger.info('----------------------------测试不同约束等级下的外键操作 期望:操作成功-----------------------------')
        sql_cmd = '''
                    delete from pteacher_table_02 where t_date = date '2020-09-01'; 
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn("violates foreign key constraint", msg)
        logger.info(msg)

        sql_cmd = '''             
                    delete from pclass_table_02 where c_date = date '2020-09-04';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn("violates foreign key constraint", msg)
        logger.info(msg)

        sql_cmd = '''
                    update pteacher_table_02 set t_date = date '2020-09-08' where t_date = date '2020-09-01';
                    select t_date from pstudent_table_02 where s_name='张三';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn("2020-09-08", msg)
        logger.info(msg)

        sql_cmd = '''
                    update pclass_table_02 set c_date = date '2020-09-09' where c_date = date '2020-09-02';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        self.assertIn("violates foreign key constraint", msg)
        logger.info(msg)

    def tearDown(self):
        logger.info('----------------------------删除表和数据库-----------------------------')
        sql_cmd = '''
                    drop table pclass_table_02 cascade;
                    drop table pteacher_table_02 cascade;
                    drop table pstudent_table_02 cascade;
                    drop database if exists pguser;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        logger.info('----------------------------Opengauss_Function_DDL_Parttion_Case0064执行完成-----------------------------')