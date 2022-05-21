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

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class LockFile(unittest.TestCase):
    def setUp(self):
        logger.info(f'------{os.path.basename(__file__)}开始执行------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_lock_file(self):
        logger.info('------创建测试表并插入数据------')
        sql_cmd = '''drop table if exists testzl;
            CREATE TABLE testzl(SK INTEGER,ID CHAR(16),
            NAME VARCHAR(20),SQ_FT INTEGER);
            insert into testzl values (001,'sk1','tt',3332);
            '''
        excute_res = self.sh_primy.execut_db_sql(sql_cmd)
        logger.info(excute_res)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, excute_res)

        logger.info('------查看视图PG_LOCKS，统计锁信息------')
        sql_cmd = '''select count(*) from PG_LOCKS 
            where mode = 'ShareRowExclusiveLock' or 
            mode = 'ShareUpdateExclusiveLock';'''
        excute_res = self.sh_primy.execut_db_sql(sql_cmd)
        logger.info(excute_res)
        self.assertNotIn('ERROR', excute_res, '查询结果失败')
        self.lock_count = excute_res.splitlines()[-2].strip()
        logger.info(excute_res)

        logger.info('------开启事务，对数据库表为测试表加SHARE ROW EXCLUSIVE锁\
                    与SHARE UPDATE EXCLUSIVE锁------')
        sql_cmd = '''
            start transaction;
            LOCK TABLE testzl IN SHARE ROW EXCLUSIVE MODE;
            LOCK TABLE testzl IN SHARE UPDATE EXCLUSIVE MODE;
            select count(*) from PG_LOCKS where 
            mode = 'ShareUpdateExclusiveLock' or mode = 'ShareRowExclusiveLock';
                    '''
        excute_res = self.sh_primy.execut_db_sql(sql_cmd)
        logger.info(excute_res)
        self.assertNotIn('ERROR', excute_res, '查询结果失败')
        self.lock_count2 = excute_res.splitlines()[-2].strip()
        self.assertIn(self.Constant.LOCK_TABLE_MSG, excute_res)

        logger.info('------进行校验------')
        sql_cmd = f'select {self.lock_count2}-{self.lock_count} as result;'
        excute_res = self.sh_primy.execut_db_sql(sql_cmd)
        logger.info(excute_res)
        self.assertNotIn('ERROR', excute_res, '查询结果失败')
        res = excute_res.splitlines()[-2].strip()
        self.assertIn('2', res)
        logger.info(res)

    def tearDown(self):
        logger.info('------清理环境------')
        sql_cmd = 'drop table if exists testzl;'
        excute_res = self.sh_primy.execut_db_sql(sql_cmd)
        logger.info(excute_res)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, excute_res)
        logger.info(f'------{os.path.basename(__file__)}执行完成------')
