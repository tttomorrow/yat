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
Case Type   : 事务控制
Case Name   : 开启事务执行select语句后是否可以再次设置事务隔离级别
Description : 1.创建测试表 2.以默认方式开启事务后执行select语句 3.重新开启事务隔离级别为REPEATABLE READ的事务隔离级别
Expect      :
    1.创建测试表成功
    2.以默认方式开启事务后执行select语句成功
    3.重新开启事务隔离级别为REPEATABLE READ的事务隔离级别失败
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info('----------------------Opengauss_Function_DML_Transaction_Case0018开始执行------------------------')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_transaction_file(self):
        logger.info('------------------------创建测试表并插入数据--------------------')
        sql_cmd = '''drop table if exists testzl;
                            CREATE TABLE testzl(SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
                            insert into testzl values (001,'sk1','tt',3332);
                            insert into testzl values (001,'sk1','tt',3332);
                            insert into testzl values (001,'sk1','tt',3332);
                            '''
        excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                            '''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg)

        logger.info('--------以默认方式开启数据库进行select后重新开启事务隔离级别为REPEATABLE READ的事务隔离级别----------------------')
        sql_cmd = f'''start transaction;
                      select * from testzl;
                      START TRANSACTION ISOLATION LEVEL REPEATABLE READ;'''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.START_TRANSACTION_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.SET_TRANSACTION_ERROR_MSG, msg)

    def tearDown(self):
        logger.info('----------------清理环境-----------------------')
        sql_cmd = 'drop table if exists testzl;'
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('----------------------Opengauss_Function_DML_Transaction_Case0018执行完成--------------------')
