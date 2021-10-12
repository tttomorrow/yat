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
Case Name   : 对数据库表加SHARE UPDATE EXCLUSIVE锁后执行垃圾回收命令（VACUUM ）
Description :
    1.创建测试表并插入数据
    2.开启事务，对表加SHARE UPDATE EXCLUSIVE锁 ,执行VACUUM操作
    3.查看视图PG_LOCKS，是否有多个SHARE ROW EXCLUSIVE锁产生
Expect      :
    1.创建测试表并插入数据成功
    2.开启事务，对表多次加ACCESS SHARE锁成功
    3.查看视图PG_LOCKS，只有一个SHARE ROW EXCLUSIVE锁产生
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
        logger.info('-------------------------Opengauss_Function_DML_Lock_Case0104开始执行-------------------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def LockFile(self):
        logger.info('----------------------------创建测试表并插入数据-----------------------------')
        sql_cmd = '''drop table if exists testzl;
                    CREATE TABLE testzl(SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
                    insert into testzl values (001,'sk1','tt',3332);
                    '''
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.userNode.db_user} -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg)

        logger.info('-----------------开启事务，对表加SHARE UPDATE EXCLUSIVE锁，执行VACUUM操作----------------')
        sql_cmd = '''
                    start transaction;
                    LOCK TABLE testzl IN SHARE UPDATE EXCLUSIVE MODE;
                    select count(*) from PG_LOCKS where mode = 'ShareUpdateExclusiveLock' and locktype = 'relation';
                    VACUUM testzl;
                    '''
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.userNode.db_user} -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.VACUUM_TRANSACTION_FAIL_MSG, msg)
        logger.info(msg)

        logger.info('-----------------查看视图PG_LOCKS，是否有多个SHARE ROW EXCLUSIVE锁产生----------------')
        sql_cmd = '''select locktype,database,relation,transactionid,classid,virtualtransaction,pid,sessionid,mode,granted,fastpath from PG_LOCKS;'''
        excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.userNode.db_user} -p {self.userNode.db_port} -c "{sql_cmd}"
                            '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)

    def tearDown(self):
        logger.info('----------------------------清理环境-----------------------------')
        sql_cmd = 'drop table if exists testzl;'
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_user} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('------------------------Opengauss_Function_DML_Lock_Case0104执行完成------------------------')
