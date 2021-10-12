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
Case Name   : 输入不属于同一个类型范畴:报错:兼容TD不会报错
Description :
    1.在A模式下，创建A兼容模式的数据库a_1。
    2.切换数据库为a_1。
    3.创建表t1。
    4.查看coalesce参数输入int和varchar类型的查询语句的执行计划。   期望:报错
    5.删除表。
    6.切换数据库为postgres。
    7.在TD模式下，创建TD兼容模式的数据库td_1。
    8.切换数据库为td_1。
    9.创建表t2。
    10.查看coalesce参数输入int和varchar类型的查询语句的执行计划。 期望:查询成功
    11.删除表。
    12.切换数据库为postgres。
    13.删除A和TD模式的数据库。
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
            '----------------------------Opengauss_Function_Cast_Case0035开始执行-----------------------------')
        self.userNode = Node('dbuser')

        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_Index_file_damaged(self):
        logger.info('----------------------------在A模式下，创建A兼容模式的数据库pguser 期望:数据库创建成功-----------------------------')
        sql_cmd = '''
                    drop database if exists pguser;
                    CREATE DATABASE pguser dbcompatibility = 'A';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, msg)

        logger.info('----------------------------创建表t1 期望:创建成功----------------------------')
        sql_cmd = '''
                    drop table if exists t1;
                    CREATE TABLE t1(a int, b varchar(10));
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

        logger.info('----------------------------查看coalesce参数输入int和varchar类型的查询语句的执行计划。 期望:报错-----------------------------')
        sql_cmd = '''
                    EXPLAIN SELECT coalesce(a, b) FROM t1;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('----------------------------删除表-----------------------------')
        sql_cmd = """
                    drop table t1 CASCADE;
                    """
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info(msg)

        logger.info('-------------------------在TD模式下，创建TD兼容模式的数据库pguser 期望:创建成功-------------------------')
        sql_cmd = '''
                    drop database if exists pguser;
                    CREATE DATABASE pguser dbcompatibility = 'C';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.DROP_DATABASE_SUCCESS, msg)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, msg)
        logger.info(msg)

        logger.info('----------------------------创建表 期望:创建成功-----------------------------')
        sql_cmd = """
                    drop table if exists t2 CASCADE;
                    CREATE TABLE t2(a int, b varchar(10));
                    """
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info(msg)

        logger.info('----------------------------查看coalesce参数输入int和varchar类型的查询语句的执行计划。 期望:查询成功-----------------------------')
        sql_cmd = """
                    EXPLAIN VERBOSE select coalesce(a, b) from t2;
                    """
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn("Output", msg)
        logger.info(msg)

        logger.info('----------------------------删除表 期望:删除成功-----------------------------')
        sql_cmd = """
                    drop table t2 CASCADE;
                    """
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info(msg)

        logger.info('-------------------------删除数据库 期望:删除成功-------------------------')
        sql_cmd = '''
                    drop database if exists pguser;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.DROP_DATABASE_SUCCESS, msg)
        logger.info(msg)

    def tearDown(self):
        # 删除表
        logger.info('----------------------------清理环境-----------------------------')
        logger.info('----------------------------no need to clean-----------------------------')
        logger.info('----------------------------Opengauss_Function_Cast_Case0035执行完成-----------------------------')