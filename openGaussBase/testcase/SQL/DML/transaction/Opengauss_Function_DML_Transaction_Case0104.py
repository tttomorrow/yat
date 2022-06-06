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
Case Type   : 事务控制
Case Name   : 不开启事务，设置local级事务隔离级别
Description :
    1.不开启事务，设置local事务隔离级别为REPEATABLE READ
    2.查看设置的事务隔离级别
Expect      :
    1.不开启事务，设置local事务隔离级别为REPEATABLE READ未报错
    2.查看设置的事务隔离级别，数据库参数显示未生效
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info('--------------------Opengauss_Function_DML_Transaction_Case0104开始执行--------------------')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_transaction_file(self):
        logger.info('------------不开启事务，设置local事务隔离级别为REPEATABLE READ----------------')
        sql_cmd = '''
                    SET LOCAL TRANSACTION ISOLATION LEVEL REPEATABLE READ ;
                    show transaction_isolation;
                    '''
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.REPEATABLE_READ_MSG, msg)

    def tearDown(self):
        logger.info('----------------无需清理环境-----------------------')
        logger.info('----------------------Opengauss_Function_DML_Transaction_Case0104执行完成--------------------')
