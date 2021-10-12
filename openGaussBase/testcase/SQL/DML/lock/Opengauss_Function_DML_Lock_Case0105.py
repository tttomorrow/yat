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
Case Name   : 同一事务的同一张表加SHARE ROW EXCLUSIVE与SHARE UPDATE EXCLUSIVE是否成功
Description :
    1.创建测试表并插入数据
    2.统计锁信息
    3.开启事务，为测试表加SHARE ROW EXCLUSIVE锁与SHARE UPDATE EXCLUSIVE锁
    4.再次统计锁信息
    5.进行校验
Expect      :
    1.创建测试表并插入数据成功
    2.统计锁信息成功
    3.开启事务，为测试表加SHARE ROW EXCLUSIVE锁与SHARE UPDATE EXCLUSIVE锁成功
    4.再次统计锁信息成功
    5.进行校验成功
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
        logger.info('----------------------------Opengauss_Function_DML_Lock_Case0105开始执行-----------------------------')
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
        sql_cmd = '''select count(*) from PG_LOCKS where mode = 'ShareRowExclusiveLock' or mode = 'ShareUpdateExclusiveLock';'''
        excute_cmd = f'''
                                        source {self.DB_ENV_PATH} ;
                                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.lock_count = msg.splitlines()[-2].strip()
        logger.info(msg)

        logger.info('-----------开启事务，对数据库表为测试表加SHARE ROW EXCLUSIVE锁与SHARE UPDATE EXCLUSIVE锁-----')
        sql_cmd = '''
                    start transaction;
                    LOCK TABLE testzl IN SHARE ROW EXCLUSIVE MODE;
                    LOCK TABLE testzl IN SHARE UPDATE EXCLUSIVE MODE;
                    select count(*) from PG_LOCKS where mode = 'ShareUpdateExclusiveLock' or mode = 'ShareRowExclusiveLock';
                    '''
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.lock_count2 = msg.splitlines()[-2].strip()
        logger.info(msg)
        self.assertIn(self.Constant.LOCK_TABLE_MSG, msg)

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
        self.assertIn('2', res)
        logger.info(res)

    def tearDown(self):
        logger.info('----------------------------清理环境-----------------------------')
        sql_cmd = 'drop table if exists testzl;'
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('-------------------------Opengauss_Function_DML_Lock_Case0105执行完成-------------------------')