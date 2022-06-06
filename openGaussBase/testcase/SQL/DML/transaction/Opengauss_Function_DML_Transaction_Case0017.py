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
Case Name   : 开启事务未执行数据修改语句后是否可以再次设置事务隔离级别
Description : 1.以默认方式开启事务 2.重新开启事务隔离级别为REPEATABLE READ的事务隔离级别 3.查看当前事务隔离级别是否为新的事务隔离级别REPEATABLE READ
Expect      :
    1.以默认方式开启事务成功
    2.重新开启事务隔离级别为REPEATABLE READ的事务隔离级别成功
    3.查看当前事务隔离级别是新的事务隔离级别REPEATABLE READ，事务隔离级别再次设置成功
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
        logger.info('----------------------Opengauss_Function_DML_Transaction_Case0017开始执行-----------------------')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_transaction_file(self):
        logger.info('----------------------开启事务不指定事务隔离级别，查看当前事务隔离级别----------------------')
        sql_cmd = f'''start transaction;
                      START TRANSACTION ISOLATION LEVEL REPEATABLE READ;
                      show transaction_isolation;'''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.PrimaryNode.db_name} -p {self.PrimaryNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.START_TRANSACTION_SUCCESS_MSG, msg)
        self.assertIn(self.Constant.REPEATABLE_READ_MSG, msg)

    def tearDown(self):
        logger.info('----------------无需清理环境-----------------------')
        logger.info('----------------------Opengauss_Function_DML_Transaction_Case0017执行完成--------------------')
