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
Case Name   : root用户文本格式导出指定的数据库
Description :
    1.连接数据库：
    2.创建数据库test：
    3.切换到创建的数据库
    4.创建表并插入数据
    5.退出数据库
    6.切换到root用户：
    7.source环境变量:
    8.root用户文本格式导出指定的数据库
Expect      :
    1.数据库连接成功
    2.创建数据库test成功
    3.切换到数据库test成功
    4.创建表并插入数据成功
    5.退出数据库
    6.切换用户
    7.source环境变量
    8.导出失败(需要omm用户执行)
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
        LOG.info('----Opengauss_Function_Tools_gs_dump_Case0005start----')
        self.dbuser_node = Node('dbuser')
        self.root_node = Node('default')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('----连接数据库并创建数据库-----------')
        sql_cmd1 = '''  drop database if exists test;
                        create database test;
                        '''
        excute_cmd1 = f'''source {macro.DB_ENV_PATH} ;
        gsql -d {self.dbuser_node.db_name} -p {self.dbuser_node.db_port}\
        -c " {sql_cmd1}"
                                '''
        LOG.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg1)

        LOG.info('-----在创建好的数据库中创建表并插入数据-----')
        sql_cmd2 = '''  create table test1 (id int ,name char(10));
                        insert into test1 values (1,'aa'),(2,'bb');
                                '''
        excute_cmd2 = f'''source {macro.DB_ENV_PATH} ;
                 gsql -d test -p {self.dbuser_node.db_port} -c "{sql_cmd2}"
                      '''
        LOG.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg2)
        LOG.info('----root用户文本格式导出指定的数据库:失败-----')
        cmd = f''' 
                source  {macro.DB_ENV_PATH} ;
                expect <<EOF
                spawn gs_dump -p {self.dbuser_node.db_port} test --format=p
                expect "Password:"
                send "{self.root_node.ssh_password}\r"
                expect eof
                '''
        LOG.info(cmd)
        msg3 = self.root_node.sh(cmd).result()
        LOG.info(msg3)
        self.assertIn('failed', msg3)

    def tearDown(self):
        LOG.info('-----------------清理环境：删除数据库-----------------')
        sql_cmd4 = '''  drop database if exists test; '''
        excute_cmd4 = f'''source {macro.DB_ENV_PATH} ;
                          gsql -d {self.dbuser_node.db_name} \
                          -p {self.dbuser_node.db_port} -c "{sql_cmd4}"
                                        '''
        LOG.info(excute_cmd4)
        msg4 = self.dbuser_node.sh(excute_cmd4).result()
        LOG.info(msg4)
        LOG.info('---Opengauss_Function_Tools_gs_dump_Case0005finish-----')
