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
Case Name   : 对表进行REINDEX时是否产生AccessExclusiveLock锁
Description :
    1.创建测试表并插入数据后创建索引
    2.统计锁信息
    3.开启事务，对测试表进行REINDEX，不做提交,统计锁信息
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

Log = Logger()


class LockFile(unittest.TestCase):
    def setUp(self):
        Log.info('-----Opengauss_Function_DML_Lock_Case0114开始执行-----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_lock_file(self):
        Log.info('------创建测试表并插入数据------')
        sql_cmd = f'drop table if exists testzl;' \
            f'CREATE TABLE testzl(SK INTEGER,ID CHAR(16),NAME VARCHAR(20),' \
            f'SQ_FT INTEGER);insert into testzl values ' \
            f'(001,\'sk1\',\'tt\',3332);CREATE INDEX ' \
            f'testzl_index ON testzl(sk);'
        excute_cmd = f'source {self.DB_ENV_PATH} ;' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -c "{sql_cmd}" '
        Log.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS_MSG, msg)

        Log.info('------查看视图PG_LOCKS，统计锁信息------')
        sql_cmd = f'select locktype,database,relation,transactionid,' \
            f'classid,mode from PG_LOCKS;' \
            f'select count(*) from PG_LOCKS where ' \
            f'mode = \'AccessExclusiveLock\' and locktype = \'relation\'; '
        excute_cmd = f'source {self.DB_ENV_PATH} ;' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -c "{sql_cmd}" '
        Log.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.lock_count = msg.splitlines()[-2].strip()
        Log.info(msg)

        Log.info('------开启事务，执行语句并统计锁信息并统计锁信息------')
        sql_cmd = f'start transaction;' \
            f'REINDEX INDEX testzl_index;' \
            f'select locktype,database,relation,transactionid,' \
            f'classid,mode from PG_LOCKS;' \
            f'select count(*) from PG_LOCKS where' \
            f' mode = \'AccessExclusiveLock\' and locktype = \'relation\';'
        excute_cmd = f'source {self.DB_ENV_PATH} ;' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -c "{sql_cmd}" '
        Log.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.lock_count2 = msg.splitlines()[-2].strip()
        Log.info(msg)
        self.assertIn(self.Constant.REINDEX_SUCCESS_MSG, msg)

        Log.info('---------------进行校验--------------')
        sql_cmd = f'select {self.lock_count2}-{self.lock_count}' \
            f' from sys_dummy;'
        excute_cmd = f'source {self.DB_ENV_PATH} ;' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -c "{sql_cmd}" '
        Log.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        Log.info(msg)
        res = msg.splitlines()[-2].strip()
        self.assertNotIn('0', res)
        Log.info(res)

    def tearDown(self):
        Log.info('------------清理环境-------------')
        sql_cmd = 'drop table if exists testzl;'
        excute_cmd = f'source {self.DB_ENV_PATH} ;' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -c "{sql_cmd}" '
        Log.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        Log.info('---Opengauss_Function_DML_Lock_Case0114执行完成---')
