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
Case Name   : 指定创建转储使用的角色名（不设置角色密码）
Description :
    1.连接数据库：
    2.创建数据
    3.退出数据库
    4.source环境变量
    5.指定创建转储使用的角色名（不设置角色密码）
    6.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据成功
    3.退出数据库
    4.source环境变量
    5.导出是失败
    6.清理环境成功
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
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0064start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.gs_dumpall_msg = 'options --role --rolepassword' \
                              ' need use together'

    def test_server_tools(self):
        LOG.info('------------创建数据-------------')
        sql_cmd1 = '''drop table if exists test1; 
            create table test1 (id int ,name char(10));
            insert into test1 values (1,'aa'),(2,'bb');
            drop user if exists user1; 
            drop user if exists user2; 
            create user user1 identified by 'qwer@123';
            create user user2 identified by 'qwer@123';
            grant all privileges to user1;
            grant user1 to user2;
            '''
        gsql_cmd1 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} -p\
            {self.dbuser_node.db_port} -c "{sql_cmd1}"
            '''
        LOG.info(gsql_cmd1)
        sql_msg1 = self.dbuser_node.sh(gsql_cmd1).result()
        LOG.info(sql_msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_msg1)

        LOG.info('--指定创建转储使用的角色名（不设置角色密码）--')
        dumpall_cmd = f'''source {macro.DB_ENV_PATH} ;
            gs_dumpall -p {self.dbuser_node.db_port} -U user2 -W qwer@123\
            -f {macro.DB_INSTANCE_PATH}/dumpall.sql --role user1;
            '''
        LOG.info(dumpall_cmd)
        dumpall_msg = self.dbuser_node.sh(dumpall_cmd).result()
        LOG.info(dumpall_msg)
        self.assertIn(self.gs_dumpall_msg, dumpall_msg)

    def tearDown(self):
        LOG.info('---清理环境---')
        sql_cmd2 = '''drop user  user1; 
            drop user  user2; 
            drop table test1;
            '''
        clear_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port} -c "{sql_cmd2}";
            '''
        LOG.info(clear_cmd)
        clear_msg = self.dbuser_node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0064finish----')
