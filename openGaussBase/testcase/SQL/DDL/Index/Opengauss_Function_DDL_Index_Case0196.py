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
Case Name   : 事务块中执行 REINDEX DATABASE重建索引
Description :
    1.创建兼容PG的数据库
    2.建表建索引
    3.设置索引不可用
    4.在事务块中执行REINDEX DATABASE
    5.查询索引不生效
    6.清理环境
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
        logger.info('----------------------------Opengauss_Function_DDL_Index_Case0196开始执行-----------------------------')
        self.userNode = Node('dbuser')

        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_Index_file_damaged(self):
        logger.info('----------------------------创建兼容PG的数据库-----------------------------')
        sql_cmd = '''drop database if exists pguser;create database pguser DBCOMPATIBILITY 'PG';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, msg)
        
        # 建表建索引
        logger.info('----------------------------建表建索引-----------------------------')
        sql_cmd = '''DROP TABLE if EXISTS test_index_table_196_01 CASCADE;
        create table test_index_table_196_01(
        c_int int,
        c_point point) WITH (ORIENTATION = row);
        
        drop index if exists index_196_01;
        drop index if exists index_196_02;
        create index index_196_01 on test_index_table_196_01(c_int);
        explain select * from test_index_table_196_01 where c_int > 500;
        create index index_196_02 on test_index_table_196_01 using gist(c_point);
        explain select * from test_index_table_196_01 where c_point <^ point(50,50);
        
        DROP TABLE if EXISTS test_index_table_196_02 CASCADE;
        create table test_index_table_196_02(
        c_int int
        ) WITH (ORIENTATION = row) partition by range(c_int)(
        partition p1 values less than (100),
        partition p2 values less than (1000),
        partition p3 values less than (5000),
        partition p4 values less than (10001)
        );
        
        drop index if exists index_196_03;
        create index index_196_03 on test_index_table_196_02(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
        explain select * from test_index_table_196_02 where c_int > 500 group by c_int;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.INDEX_BITMAP_SUCCESS_MSG, msg)

        # 设置索引不可用
        logger.info('----------------------------设置索引不可用-----------------------------')
        sql_cmd = '''alter index index_196_01  UNUSABLE;
        alter index index_196_02  UNUSABLE;
        alter index index_196_03  UNUSABLE;
        explain select * from test_index_table_196_01 where c_int > 500;
        explain select * from test_index_table_196_01 where c_point <^ point(50,50);
        explain select * from test_index_table_196_02 where c_int > 500 group by c_int;'''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.ALTER_INDEX_SUCCESS_MSG,msg)
        self.assertNotIn(self.Constant.INDEX_BITMAP_SUCCESS_MSG, msg)
        logger.info(msg)

        # 在事务块中执行REINDEX DATABASE
        logger.info('----------------------------在事务块中执行REINDEX DATABASE-----------------------------')
        sql_cmd="""begin
                    REINDEX DATABASE pguser;
                 end;
        """
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn("cannot be executed from a function or multi-command string",msg)
        logger.info(msg)

        # 在事务块中执行REINDEX DATABASE
        logger.info('----------------------------查询索引不生效-----------------------------')
        sql_cmd = '''explain select * from test_index_table_196_01 where c_int > 500;
        explain select * from test_index_table_196_01 where c_point <^ point(50,50);
        explain select * from test_index_table_196_02 where c_int > 500 group by c_int;'''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertNotIn(self.Constant.INDEX_BITMAP_SUCCESS_MSG, msg)
        logger.info(msg)

    def tearDown(self):
        # 删除表
        logger.info('----------------------------删除表-----------------------------')
        sql_cmd = '''DROP TABLE if EXISTS test_index_table_196_01 CASCADE;
        DROP TABLE if EXISTS test_index_table_196_02 CASCADE;'''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)

        #删除数据库
        logger.info('----------------------------删除兼容PG的数据库-----------------------------')
        sql_cmd = '''drop database if exists pguser;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        logger.info('----------------------------Opengauss_Function_DDL_Index_Case0196执行完成-----------------------------')