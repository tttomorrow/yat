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
Case Type   : 服务端工具
Case Name   : 转储过程中使用可串行化事务，是否可以导出数据
Description :
    1.连接数据库
    2.创建数据库test
    3.切换到数据库test
    4.创建表插入数据
    5.退出数据库
    6.source环境变量
    7.转储过程中使用可串行化事务，是否可以导出数据
    8.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据库test成功
    3.切换到数据库test
    4.创建表成功
    5.退出数据库
    6.source环境变量
    7.导出成功
    8.清理环境成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('----Opengauss_Function_Tools_gs_dump_Case0061start------')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('----------------连接数据库并创建数据库----------------')
        sql_cmd1 = '''drop database if exists testdump;
            create database testdump;
            '''
        excute_cmd1 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port} -c "{sql_cmd1}"
            '''
        LOG.info(excute_cmd1)
        sql_msg1 = self.dbuser_node.sh(excute_cmd1).result()
        LOG.info(sql_msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_msg1)
        LOG.info('--------------------创建数据--------------------')
        sql_cmd2 = '''drop table  if exists t1;
            create table t1 (i int,d int );
            insert into t1 values(1,2),(2,3),(3,4);
            '''
        excute_cmd2 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d testdump -p {self.dbuser_node.db_port} -c "{sql_cmd2}"
            '''
        LOG.info(excute_cmd2)
        sql_msg2 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(sql_msg2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_msg2)
        LOG.info('-------转储过程中使用可串行化事务，是否可以导出数据---------')
        dump_cmd = f'source {macro.DB_ENV_PATH} ;' \
            f'gs_dump  ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'testdump ' \
            f'--format=p ' \
            f'--serializable-deferrable;'
        LOG.info(dump_cmd)
        dump_msg = self.dbuser_node.sh(dump_cmd).result()
        LOG.info(dump_msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, dump_msg)
        self.assertIn('CREATE TABLE t1', dump_msg)
        self.assertIn('COPY t1 (i, d) FROM stdin;', dump_msg)


    def tearDown(self):
        LOG.info('-----------------清理环境：删除数据库-----------------')
        sql_cmd3 = '''drop database if exists testdump; '''
        excute_cmd3 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port} -c "{sql_cmd3}";
            '''
        LOG.info(excute_cmd3)
        clear_msg = self.dbuser_node.sh(excute_cmd3).result()
        LOG.info(clear_msg)
        LOG.info('---Opengauss_Function_Tools_gs_dump_Case0061finish---')


