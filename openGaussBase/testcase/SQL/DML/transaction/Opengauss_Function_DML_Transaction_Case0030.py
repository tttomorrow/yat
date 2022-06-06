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
Case Name   : 输入位串类型的变量，匿名块正常执行,匿名块中事务是否同步到主机
Description :
    1.新建测试表
    2.在匿名块中写入位串类型的变量，对数据库表执行插入操作
    3.查看主机事务数据
    4.查看备机事务数据
Expect      :
    1.创建测试表成功
    2.在匿名块中写入位串类型的变量，对数据库表执行插入操作成功
    3.主机事务数据同步成功
    4.备机事务数据同步成功
History     : 
"""

import os
import unittest
from yat.test import Node
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger

logger = Logger()


@unittest.skipIf(1 >= CommonSH('PrimaryDbUser').get_node_num(), '单机环境不执行')
class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info(f'-----{os.path.basename(__file__)[:-3]}开始执行-----')
        self.primary_node = Node('PrimaryDbUser')
        self.primary_sh_node = CommonSH('PrimaryDbUser')
        self.standby1_sh_node = CommonSH('Standby1DbUser')
        self.com = Common()
        self.Constant = Constant()
        self.tb_name = 'test_trans_0030'

    def test_transaction_file(self):
        logger.info('-----step1:创建测试表;expect:创建成功-----')
        sql_cmd = f'drop table if exists {self.tb_name};' \
                  f'create table {self.tb_name}' \
                  f'(c_bit bit(3),c_bitvaring bit varying(5));'
        msg = self.primary_sh_node.execut_db_sql(sql_cmd,
                dbname=f'{self.primary_node.db_name}')
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

        logger.info('-----step2:在匿名块中写入位串类型的变量，对数据库表执行插入操作;expect:插入成功-----')
        sql_cmd = f'''  declare 
                          a bit(3);
                          b bit varying(5) ;
                        begin
                          a := B'101';
                          b := B'00';
                          insert into {self.tb_name} values (a,b);
                        end;
                     '''
        msg = self.primary_sh_node.execut_db_sql(sql_cmd,
                dbname=f'{self.primary_node.db_name}')
        logger.info(msg)
        self.assertIn(self.Constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG, msg)

        logger.info('-----step3:查看主机数据;expect:1-----')
        sql_cmd = f'''select count(*) from {self.tb_name};'''
        msg = self.primary_sh_node.execut_db_sql(sql_cmd,
                dbname=f'{self.primary_node.db_name}')
        logger.info(msg)
        res = msg.splitlines()[-2].strip()
        self.assertIn('1', res)

        logger.info('----等待备机完成数据同步----')
        node_num = self.com.get_node_num(self.primary_node)
        logger.info(node_num)
        consistency_flag = self.primary_sh_node.check_location_consistency(
                                                                'primary',
                                                                 node_num,
                                                                 300)
        self.assertTrue(consistency_flag)

        logger.info('-----step4:查看备机数据;expect:1-----')
        msg = self.standby1_sh_node.execut_db_sql(sql_cmd,
                dbname=f'{self.primary_node.db_name}')
        logger.info(msg)
        res = msg.splitlines()[-2].strip()
        self.assertIn('1', res)

    def tearDown(self):
        logger.info('-----清理环境-----')
        sql_cmd = f'drop table if exists {self.tb_name};'
        msg = self.primary_sh_node.execut_db_sql(sql_cmd,
                dbname=f'{self.primary_node.db_name}')
        logger.info(msg)
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info(f'-----{os.path.basename(__file__)[:-3]}执行完成-----')
