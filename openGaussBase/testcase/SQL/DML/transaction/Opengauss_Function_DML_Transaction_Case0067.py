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
Case Name   : 开启事务执行事务后使用rollback命令使事务回滚，查看备机数据
Description :
    1.创建测试表成功
    2.开启事务并执行事务成功
    3.执行rollback命令对事务进行回滚成功
    4.查看备机事务数据回滚成功
Expect      :
    1.创建测试表成功
    2.开启事务并执行事务成功
    3.执行rollback命令对事务进行回滚成功
    4.查看备机事务数据回滚成功
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info('--------------------Opengauss_Function_DML_Transaction_Case0067开始执行--------------------')
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
            logger.info('------------------------新建测试表--------------------')
            sql_cmd = '''drop table if exists testzl;
                        create table testzl (SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
                        '''
            excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                        '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

            logger.info('--------------使用BEGIN开启事务后使用ROLLBACK进行回滚-------------')
            sql_cmd = f'''BEGIN ;
                          insert into testzl values (001,'sk1','tt',3332);
                          ROLLBACK;'''
            excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                            '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.ROLLBACK_MSG, msg)

            logger.info('---------------------查看备机数据是否同步----------------------')
            sql_cmd = f'''select count(*) from testzl;'''
            excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.StandbyNode.db_name} -p {self.StandbyNode.db_port} -c "{sql_cmd}"
                            '''
            logger.info(excute_cmd)
            msg = self.StandbyNode.sh(excute_cmd).result()
            logger.info(msg)
            res = msg.splitlines()[-2].strip()
            self.assertIn('0', res)

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
        logger.info('----------------------Opengauss_Function_DML_Transaction_Case0067执行完成--------------------')
