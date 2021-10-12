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
Case Type   : 锁定表
Case Name   : 对表进行VACUUM FULL时是否产生AccessExclusiveLock锁
Description :
    1.创建测试表并插入数据后创建索引
    2.统计锁信息
    3.开启事务，对测试表进行VACUUM FULL，不做提交,统计锁信息
    4.进行校验
    5.清理环境
Expect      :
    1.创建测试表及索引并插入数据成功
    2.查看视图PG_LOCKS，统计锁信息成功
    3.开启事务，执行语句
    4.统计锁信息成功，事务产生AccessExclusiveLock锁
    5.清理环境成功
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
        logger.info('----------------------------Opengauss_Function_DML_Lock_Case0115开始执行-----------------------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_lock_file(self):
        logger.info('----------------------------创建测试表并插入数据-----------------------------')
        sql_cmd = '''drop table if exists testzl;
                    CREATE TABLE testzl(SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
                    insert into testzl values (001,'sk1','tt',3332);
                    '''
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg)

        logger.info('----------------------------查看视图PG_LOCKS，统计锁信息-----------------------------')
        sql_cmd = '''select locktype,database,relation,transactionid,classid,mode from PG_LOCKS;
                    select count(*) from PG_LOCKS where mode = 'AccessExclusiveLock' and locktype = 'relation'; 
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.lock_count = msg.splitlines()[-2].strip()
        logger.info(msg)

        logger.info('-----------------开启事务，执行语句并统计锁信息并统计锁信息----------------')
        sql_cmd = '''
                    start transaction;
                    VACUUM FULL testzl ;
                    select locktype,database,relation,transactionid,classid,mode from PG_LOCKS;
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
        self.assertIn(self.Constant.VACUUM_SUCCESS_MSG, msg)

        logger.info('---------------------------进行校验---------------------------')
        sql_cmd = f'select {self.lock_count2}-{self.lock_count} from dual;'
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        res = msg.splitlines()[-2].strip()
        self.assertNotIn('0', res)
        logger.info(res)

    def tearDown(self):
        logger.info('----------------------------后置处理-----------------------------')
        sql_cmd = 'drop table if exists testzl;'
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('-----------------------Opengauss_Function_DML_Lock_Case0115执行完成-----------------------------')
