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
Case Name   : 将写入表数据语句放在匿名块变量中执行
Description : 1.新建测试表 2.使用匿名块对主机数据进行数据写入 3.确认写入成功-查看备机数据是否同步
Expect      : 
"""

import sys
import unittest
from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info(
            '--------------------Opengauss_Function_DML_Transaction_Case0013开始执行--------------------')
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
                        insert into testzl values (001,'sk1','tt',3332);
                        '''
            excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                        '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

            logger.info('--------------使用匿名块对主机数据进行数据写入-------------')
            sql_cmd = f'''declare 
                            v_sql varchar;
                          begin
                            v_sql := 'insert into testzl values (008,''sk1'',''tt'',3332);';
                            execute immediate v_sql ;
                          end;
                          '''
            excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                            '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG, msg)

            logger.info('-----------------查看备机数据，确认数据写入成功-------------------')
            sql_cmd = f'''select count(*) from testzl;'''
            excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.StandbyNode.db_name} -p {self.StandbyNode.db_port} -c "{sql_cmd}"
                            '''
            logger.info(excute_cmd)
            msg = self.StandbyNode.sh(excute_cmd).result()
            logger.info(msg)
            res = msg.splitlines()[-2].strip()
            self.assertIn('2', res)

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
        logger.info('-----------------------Opengauss_Function_DML_Transaction_Case0013执行完成--------------------')
