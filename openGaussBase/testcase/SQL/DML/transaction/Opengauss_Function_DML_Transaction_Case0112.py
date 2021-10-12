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
Case Name   : 在一个会话中创建事务后新开启会话提交事务
Description :
    1.开启事务并执行事务
    2.查看保存信息
    3.开启新的会话，重新连接数据库查看保存信息
    4.进行事务提交
    5.查看数据库状态
Expect      :
    1.开启事务并执行事务成功
    2.查看保存信息成功
    3.开启新的会话，重新连接数据库查看保存信息成功
    4.进行事务提交成功
    5.查看数据库状态，主备状态正常
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info('--------------------Opengauss_Function_DML_Transaction_Case0112开始执行--------------------')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.macro = macro

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
            logger.info('------------------------使用系统用户开启事务并执行事务--------------------')
            sql_cmd = '''begin;
                         drop table if exists demo;
                         create table demo (a text,b integer);
                         prepare transaction 'the first prepare transaction';
                        '''
            excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port}  -c "{sql_cmd}"
                        '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.PREPARED_TRANSACTION_MSG, msg)

            logger.info('---------------使用系统用户重新连接数据库查看保存信息,并进行事务回滚------------')
            sql_cmd = '''select * from pg_prepared_xacts;
                         commit prepared 'the first prepare transaction';'''
            excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                            '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn('the first prepare transaction', msg)
            self.assertIn(self.Constant.PREPARED_COMMIT_MSG, msg)

            logger.info('---------------------查看数据是否提交完成----------------------')
            sql_cmd = f'''select * from pg_prepared_xacts;'''
            excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                            '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertNotIn('the first prepare transaction', msg)

    def tearDown(self):
        logger.info('----------------清理环境-----------------------')
        sql_cmd = '''select * from pg_prepared_xacts;
                    commit prepared 'the first prepare transaction';
                    drop table if exists demo;'''
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('----------------------Opengauss_Function_DML_Transaction_Case0112执行完成--------------------')
