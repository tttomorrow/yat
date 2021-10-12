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
Case Name   : 参数tablespaces-postfix和binary-upgrade一起使用是否可以导出数据
Description :
    1.连接数据库：
    2.创建数据
    3.退出数据库
    4.source环境变量
    5.参数tablespaces-postfix和binary-upgrade一起使用是否可以导出数据
    6.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据成功
    3.退出数据库
    4.source环境变量
    5.导出成功
    6.清理环境成功
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
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0043start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('------------创建数据-------------')
        sql_cmd1 = '''drop table if exists test1; 
            create table test1 (id int ,name char(10));
            insert into test1 values (1,'aa'),(2,'bb');
            drop role if exists manager; 
            create role manager identified by 'qwer@123';
            drop database if exists db_test;
            create database  db_test;
            drop tablespace if exists tbspace;
            create tablespace tbspace relative location 'tbspace_qm/tbspace';
            drop schema if exists schema1;
            create schema schema1;
            '''
        gsql_cmd1 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} -p\
            {self.dbuser_node.db_port} -c "{sql_cmd1}"
            '''
        LOG.info(gsql_cmd1)
        sql_msg1 = self.dbuser_node.sh(gsql_cmd1).result()
        LOG.info(sql_msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_msg1)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_msg1)

        LOG.info('--tablespaces-postfix和binary-upgrade一起使用成功导出数据--')
        dumpall_cmd = f'''source {macro.DB_ENV_PATH} ;
            gs_dumpall -p {self.dbuser_node.db_port}\
            --tablespaces-postfix tbsp --binary-upgrade;
            '''
        LOG.info(dumpall_cmd)
        dumpall_msg = self.dbuser_node.sh(dumpall_cmd).result()
        LOG.info(dumpall_msg)
        self.assertIn(self.constant.gs_dumpall_success_msg, dumpall_msg)
        self.assertIn('For binary upgrade', dumpall_msg)

    def tearDown(self):
        LOG.info('---清理环境---')
        sql_cmd2 = '''drop table if exists test1; 
            drop role if exists manager;
            drop database if exists db_test;
            drop tablespace if exists tbspace;
            drop schema if exists schema1;
            '''
        clear_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port} -c "{sql_cmd2}";
            rm -rf {macro.DB_INSTANCE_PATH}/pg_location/tbspace_qm;
            '''
        LOG.info(clear_cmd)
        clear_msg = self.dbuser_node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0043finish----')
