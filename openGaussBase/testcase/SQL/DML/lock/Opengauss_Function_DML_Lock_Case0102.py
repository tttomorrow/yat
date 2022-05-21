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
Case Type   : 锁定表
Case Name   : 没有声明锁模式，缺省是否为模式ACCESS EXCLUSIVE
Description :
    1. 查看视图PG_LOCKS，统计锁信息
    2.开启事务，创建表,查询视图信息
    3. 进行结果校验
    4.清理环境
Expect      :
    1.查看视图PG_LOCKS，统计锁信息成功
    2.开启事务，创建表成功
    3.查询视图信息，进行校验，产生AccessExclusiveLock成功
    4.清理环境成功
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class LockFile(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Lock_Case0102开始执行--------------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def LockFile(self):
        logger.info('------------------------查看视图PG_LOCKS，统计锁信息--------------------')
        sql_cmd = '''select count(*) from PG_LOCKS where mode = 'AccessExclusiveLock' and locktype = 'relation';'''
        excute_cmd = f'''
                                source {self.DB_ENV_PATH} ;
                                gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                                '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.lock_count = msg.splitlines()[-2].strip()
        logger.info(msg)

        logger.info('----------------------开启事务，创建表,查询视图信息----------------------')
        sql_cmd = '''
                    start transaction;
                    CREATE TABLE testzl(SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
                    select count(*) from PG_LOCKS where mode = 'AccessExclusiveLock' and locktype = 'relation';
                     '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.lock_count2 = msg.splitlines()[-2].strip()
        logger.info(msg)

        logger.info('----------------------进行校验----------------------')
        sql_cmd = f'''
                    select {self.lock_count2}-{self.lock_count} from dual;
                             '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        res = msg.splitlines()[-2].strip()
        self.assertIn('1', res)
        logger.info(res)

    def tearDown(self):
        self.Constant = Constant()
        logger.info('------------------------清理环境--------------------')
        sql_cmd = 'drop table if exists testzl;'
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('------------------------Opengauss_Function_DML_Lock_Case0102执行完成--------------------')
