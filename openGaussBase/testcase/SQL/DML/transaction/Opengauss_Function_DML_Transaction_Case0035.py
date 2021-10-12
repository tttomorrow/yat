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
Case Name   : 匿名块中的自定义函数名称为重名不重参函数，并且两个函数均有入参但参数不同，匿名块提交后备机数据是否同步
Description :
    1.创建测试表
    2.创建参数类型为char的函数
    3.创建参数类型为integer的函数
    2.在匿名块中调用该函数
    3.备机事务数据同步
Expect      :
    1.创建测试表成功
    2.创建参数类型为char的函数成功
    3.创建参数类型为integer的函数成功
    2.在匿名块中调用该函数成功
    3.备机事务数据同步成功
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info('--------------------Opengauss_Function_DML_Transaction_Case0035开始执行-----------------------')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_transaction_file(self):
        logger.info('---------------------若为单机环境，后续不执行，直接通过--------------------')
        excute_cmd = f''' source {self.DB_ENV_PATH}
                       gs_om -t status --detail
                      '''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        if 'Standby' not in msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.StandbyNode = Node('Standby1DbUser')
            logger.info('------------------------创建测试表--------------------')
            sql_cmd = '''drop table if exists testzl;
                         create table testzl (sk char(10));
                         create table testzl1 (sk integer);'''
            excute_cmd = f'''
                                source {self.DB_ENV_PATH} ;
                                gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                                '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

            logger.info('----------------------创建参数类型为char的函数与参数类型为integer的函数--------------------------')
            vars = '\$$'
            sql_cmd = f'''  drop function if exists get_transaction(CHAR(16));
                            create function get_transaction(i CHAR(16)) returns CHAR(16) as {vars}
                            begin
                             return i;
                            end;
                            {vars} LANGUAGE plpgsql;
                            drop function if exists get_transaction(i integer);
                            create function get_transaction(i integer) returns integer as {vars}
                            begin
                             return i+1;
                            end;
                            {vars} LANGUAGE plpgsql;'''
            excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                        '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.CREATE_FUNCTION_SUCCESS_MSG, msg)

            logger.info('-------------在匿名块中调用参数类型为char的函数-------------')
            sql_cmd = f'''  BEGIN
                              insert into testzl values (get_transaction('aa'));
                            END;
                         '''
            excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                            '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG, msg)

            logger.info('-------------检验参数类型为char的函数是否调用成功-------------')
            sql_cmd = 'select * from testzl;'
            excute_cmd = f'''
                                    source {self.DB_ENV_PATH} ;
                                    gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                                    '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            res = msg.splitlines()[-2].strip()
            self.assertIn('aa', res)

            logger.info('------------------------在匿名块中调用参数类型为integer的函数--------------------')
            sql_cmd = f'''  BEGIN
                              insert into testzl1 values (get_transaction(1));
                            END;
                                 '''
            excute_cmd = f'''
                                    source {self.DB_ENV_PATH} ;
                                    gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                                    '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG, msg)

            logger.info('-----------------------检验参数类型为integer的函数是否调用成功-----------------------')
            sql_cmd = 'select * from testzl1;'
            excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                            '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            res = msg.splitlines()[-2].strip()
            self.assertIn('2', res)

    def tearDown(self):
        logger.info('----------------清理环境-----------------------')
        sql_cmd = '''drop table if exists testzl;
                     drop table if exists testzl1;
                     drop function get_transaction(CHAR(16));
                     drop function get_transaction(i integer);'''
        excute_cmd = f'''    
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('----------------------Opengauss_Function_DML_Transaction_Case0035执行完成------------------------')
