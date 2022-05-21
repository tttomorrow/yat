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
Case Name   : 指定事务访问模式为READ WRITE后对测试表执行写操作，执行后查看备机数据
Description : 1.创建测试表 2.开启事务指定事务访问模式为READ WRITE 后做INSERT操作 3.查看备机数据
Expect      :
    1.创建测试表成功
    2.开启事务指定事务访问模式为READ WRITE成功 INSERT操作成功
    3.备机数据同步成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
primary_sh = CommonSH('PrimaryDbUser')


class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info('----Opengauss_Function_DML_Transaction_Case0006开始执行----')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.Constant = Constant()
        self.Common = Common()
        self.table_name = 't_transaction_0006'

    def test_transaction_file(self):
        logger.info('------若为单机环境，后续不执行，直接通过------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t status --detail'''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        if 'Standby' not in msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.StandbyNode = Node('Standby1DbUser')

            text = '------step1:新建测试表;  expect:成功------'
            logger.info(text)
            sql_cmd = f'''drop table if exists {self.table_name};
                create table {self.table_name}(sk integer,id char(16),
                name varchar(20),sq_ft integer);'''
            excute_cmd = f'''source {macro.DB_ENV_PATH} ;
                gsql -d {self.PrimaryNode.db_name} \
                -p {self.PrimaryNode.db_port} \
                -c "{sql_cmd}"'''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg,
                          '执行失败' + text)

            text = '------step2:开启事务指定事务访问模式为read write后做insert操作; ' \
                   'expect:insert操作成功------'
            logger.info(text)
            sql_cmd = f'''start transaction read write;
                insert into {self.table_name} values (008,'sk1','tt',3332);
                commit;'''
            excute_cmd = f'''source {macro.DB_ENV_PATH} ;
                gsql -d {self.PrimaryNode.db_name} \
                -p {self.PrimaryNode.db_port} \
                -c "{sql_cmd}"'''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertTrue(self.Constant.START_TRANSACTION_SUCCESS_MSG in msg
                            and self.Constant.INSERT_SUCCESS_MSG in msg,
                            '执行失败' + text)

            logger.info('----等待备机完成数据同步----')
            node_num = self.Common.get_node_num(self.PrimaryNode)
            logger.info(node_num)
            consistency_flag = primary_sh.check_location_consistency('primary',
                                                                     node_num,
                                                                     300)
            self.assertTrue(consistency_flag)

            text = '------step3:查看备机数据是否同步; expect:数据同步------'
            logger.info(text)
            sql_cmd = f'''select count(*) from {self.table_name};'''
            excute_cmd = f'''source {macro.DB_ENV_PATH} ;
                gsql -d {self.StandbyNode.db_name} \
                -p {self.StandbyNode.db_port} \
                -c "{sql_cmd}"'''
            logger.info(excute_cmd)
            msg = self.StandbyNode.sh(excute_cmd).result()
            logger.info(msg)
            res = msg.splitlines()[-2].strip()
            self.assertEqual('1', res, '执行失败' + text)

    def tearDown(self):
        logger.info('------清理环境------')
        sql_cmd = f'''drop table if exists {self.table_name};'''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.PrimaryNode.db_name} \
            -p {self.PrimaryNode.db_port} \
            -c "{sql_cmd}"'''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('----Opengauss_Function_DML_Transaction_Case0006执行完成----')
