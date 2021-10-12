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
Case Name   : 使用指定的用户名连接
Description :
    1.连接数据库
    2.创建数据库test
    3.切换到数据库test
    4.创建用户，给创建的用户授权
    5.创建表并插入数据
    6.退出数据库
    7.使用指定的用户名连接（不出现密码提示）
    8.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据库test成功
    3.切换到数据库test
    4.常见用户并授权成功
    5.创建表成功
    6.退出数据库
    7.连接失败，无法导出数据
    8.清理环境成功
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('----opengauss_function_tools_gs_dump_case0085start------')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('----------------连接数据库并创建数据库----------------')
        sql_cmd1 = '''          drop database if exists test;
                                create database test;
                                '''
        excute_cmd1 = f'''      source {macro.DB_ENV_PATH} ;
                                gsql -d {self.dbuser_node.db_name}\
                                -p {self.dbuser_node.db_port} -c "{sql_cmd1}"
                                        '''
        LOG.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg1)
        LOG.info('-----在创建好的数据库中创建用户，授权并创建表插入数据----')
        sql_cmd2 = ''' 
                        drop user if exists qaz;
                        create user qaz identified by 'qwer@123';
                        grant all privileges to qaz;
                        drop table  if exists t1;
                        drop table  if exists t2;
                        create table t1 (i int,d int );
                        insert into t1 values(1,2),(2,3),(3,4);
                        create table t2 (id int,dd int);
                        insert into t2 values(11,22),(21,34),(31,45);

                        '''
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d test ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd2}"'
        LOG.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg2)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, msg2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg2)
        LOG.info('-----使用指定的用户名连接（不出现密码提示）-----')
        excute_cmd3 = f'source {macro.DB_ENV_PATH};' \
            f'gs_dump -p {self.dbuser_node.db_port} test ' \
            f'-F p -U qaz -w'
        LOG.info(excute_cmd3)
        msg3 = self.dbuser_node.sh(excute_cmd3).result()
        LOG.info(msg3)
        self.assertIn('failed', msg3)

    def tearDown(self):
        LOG.info('-----------------清理环境：删除数据库-----------------')
        sql_cmd4 = 'drop database if exists test;drop user if exists qaz; '
        excute_cmd4 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.dbuser_node.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd4}";'
        LOG.info(excute_cmd4)
        msg4 = self.dbuser_node.sh(excute_cmd4).result()
        LOG.info(msg4)
        LOG.info('----opengauss_function_tools_gs_dump_case0085finish----')
