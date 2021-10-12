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
Case Name   : 使用commit提交后'/'是否还有提交功能
Description :
    1.创建测试表成功
    2.使用BEGIN开启并执行事务成功
    3.使用COMMIT进行提交成功
    4.使用‘/’提交失败，系统会将‘/’识别为符号，而不是提交命令
Expect      :
    1.创建测试表成功
    2.使用BEGIN开启并执行事务成功
    3.使用COMMIT进行提交成功
    4.使用‘/’提交失败，系统会将‘/’识别为符号，而不是提交命令
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info('--------------------Opengauss_Function_DML_Transaction_Case0064开始执行--------------------')
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
                         create table testzl (sk integer,id char(16),name varchar(20),sq_ft integer);'''
            excute_cmd = f'''
                                source {self.DB_ENV_PATH} ;
                                gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                                '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

            logger.info('----------------------使用BEGIN开启事务并执行事务后使用commit与斜杠提交--------------------------')
            vars = '/'
            sql_cmd = f'''begin;
                          insert into test_zl values (001,'sk1','tt',3332);
                          commit;
                         {vars}'''
            excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                        '''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.COPY_SYNTAX_ERROR_MSG, msg)

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
        logger.info('----------------------Opengauss_Function_DML_Transaction_Case0064执行完成--------------------')
