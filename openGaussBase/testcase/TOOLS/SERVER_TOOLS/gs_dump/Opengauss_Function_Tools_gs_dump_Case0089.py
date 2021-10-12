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
Case Type   : 服务端工具
Case Name   : 以指定的字符集编码格式输出指定的表
Description :
    1.连接数据库：
    2.创建数据库test：
    3.切换到数据库test
    4.创建表并插入数据成功
    5.退出数据库
    6.source环境变量
    7.以指定的字符集编码格式输出指定的表
    8.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据库test成功
    3.切换到数据库test
    4.创建表并插入数据成功
    5.退出数据库
    6.source环境变量
    7.以指定的字符集编码格式输出指定的表成功
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
        LOG.info('----Opengauss_Function_Tools_gs_dump_Case0089start-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        sql_cmd1 = '''          drop database if exists test;
                                create database test;
                                        '''
        excute_cmd1 = f''' source {macro.DB_ENV_PATH} ;
                          gsql -d {self.dbuser_node.db_name}\
                          -p {self.dbuser_node.db_port} -c "{sql_cmd1}"
                                                '''
        LOG.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg1)
        LOG.info('--------在创建好的数据库中创建表并插入数据--------')
        sql_cmd2 = '''drop table  if exists t1;
                    drop table  if exists t2;
                    create table t1 (i int,d int );
                    insert into t1 values(1,2),(2,3),(3,4);
                    create table t2 (id int,dd int);
                    insert into t2 values(11,22),(21,34),(31,45);
                        '''
        excute_cmd2 = f'''source {macro.DB_ENV_PATH} ;
        gsql -d test -p {self.dbuser_node.db_port} -c "{sql_cmd2}"
                                                '''
        LOG.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg2)
        LOG.info('---------以指定的字符集编码导出指定的表:GBK----------')
        excute_cmd3 = f'''source {macro.DB_ENV_PATH} ;
        gs_dump -p {self.dbuser_node.db_port} test -F p -E GBK -t t1;'''
        LOG.info(excute_cmd3)
        msg3 = self.dbuser_node.sh(excute_cmd3).result()
        LOG.info(msg3)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg3)
        self.assertIn("SET client_encoding = 'GBK'", msg3)
        self.assertIn("CREATE TABLE t1", msg3)
        self.assertIn("COPY t1", msg3)
        LOG.info('---------以指定的字符集编码导出指定的表:UTF-8----------')
        excute_cmd4 = f'''source {macro.DB_ENV_PATH};
        gs_dump -p {self.dbuser_node.db_port} test -F p -E UTF-8 -t t1;'''
        LOG.info(excute_cmd4)
        msg4 = self.dbuser_node.sh(excute_cmd4).result()
        LOG.info(msg4)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg4)
        self.assertIn("SET client_encoding = 'UTF8'", msg4)
        self.assertIn("CREATE TABLE t1", msg4)
        self.assertIn("COPY t1", msg4)

    def tearDown(self):
        LOG.info('-----------------清理环境：删除数据库-----------------')
        sql_cmd5 = '''  drop database if exists test; '''
        excute_cmd5 = f'''source {macro.DB_ENV_PATH} ;
                        gsql -d {self.dbuser_node.db_name}\
                        -p {self.dbuser_node.db_port} -c "{sql_cmd5}";
                     '''
        LOG.info(excute_cmd5)
        msg5 = self.dbuser_node.sh(excute_cmd5).result()
        LOG.info(msg5)
        LOG.info('----Opengauss_Function_Tools_gs_dump_Case0089finish----')
