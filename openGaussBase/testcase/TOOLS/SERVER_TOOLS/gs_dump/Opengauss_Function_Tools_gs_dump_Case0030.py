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
Case Name   : 导出的文件以创建数据库和连接到创建的数据库的命
              令开始（文本格式以外的其他格式）
Description :
    1.连接数据库
    2.创建数据库
    3.切换到数据库test
    4.创建表并插入数据
    5.退出数据库
    6.source环境变量
    7.导出的文件以创建数据库和连接到创建的数据库的命令开始
    （文本格式以外的其他格式）
    8.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据库test成功
    3.切换到数据库test
    4.创建表并插入数据成功
    5.退出数据库
    6.source环境变量
    7.有清理指令，导出成功
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
        LOG.info('----Opengauss_Function_Tools_gs_dump_Case0030start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        sql_cmd1 = '''drop database if exists test;
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
        LOG.info('------在创建好的数据库中创建表并插入数据------')
        sql_cmd2 = '''drop table if exists test1; 
                    create table test1 (id int ,name char(10));
                    insert into test1 values (1,'aa'),(2,'bb');
                        '''
        excute_cmd2 = f'''source {macro.DB_ENV_PATH} ;
        gsql -d test -p {self.dbuser_node.db_port} -c "{sql_cmd2}"
                          '''
        LOG.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg2)
        LOG.info('----导出的文件以创建数据库和连接到创建的数据库\
        的命令开始（自定义格式）-----')
        excute_cmd3 = f'''source {macro.DB_ENV_PATH} ;
        gs_dump -p {self.dbuser_node.db_port} test --format=c\
        -f {macro.DB_INSTANCE_PATH}/dump_qm1 -C;
                    '''
        LOG.info(excute_cmd3)
        msg3 = self.dbuser_node.sh(excute_cmd3).result()
        LOG.info(msg3)
        execute_cmd4 = f'''du -h {macro.DB_INSTANCE_PATH}/dump_qm1'''
        msg4 = self.dbuser_node.sh(execute_cmd4).result()
        LOG.info(msg4)
        msg4_list = msg4.split()[0]
        self.assertTrue(float(msg4_list[:-1]) > 0)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg3)

        LOG.info('---------导出的文件以创建数据库和连接到\
        创建的数据库的命令开始（tar格式）----------')
        excute_cmd5 = f'''source {macro.DB_ENV_PATH} ;
        gs_dump -p {self.dbuser_node.db_port} test --format=t\
        -f {macro.DB_INSTANCE_PATH}/dump_qm2 -C;
                          '''
        LOG.info(excute_cmd5)
        msg5 = self.dbuser_node.sh(excute_cmd5).result()
        LOG.info(msg5)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg5)
        execute_cmd6 = f'''du -h {macro.DB_INSTANCE_PATH}/dump_qm2'''
        msg6 = self.dbuser_node.sh(execute_cmd6).result()
        LOG.info(msg6)
        msg6_list = msg6.split()[0]
        self.assertTrue(float(msg6_list[:-1]) > 0)

        LOG.info('----导出的文件以创建数据库和连接到创建\
        的数据库的命令开始（归档格式）-----')
        excute_cmd7 = f'''source {macro.DB_ENV_PATH} ;
                    gs_dump -p {self.dbuser_node.db_port} test --format=d\
                    -f {macro.DB_INSTANCE_PATH}/dump_qm3 -C;
                              '''
        LOG.info(excute_cmd7)
        msg7 = self.dbuser_node.sh(excute_cmd7).result()
        LOG.info(msg3)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg7)
        execute_cmd8 = f'''du -h {macro.DB_INSTANCE_PATH}/dump_qm3'''
        msg8 = self.dbuser_node.sh(execute_cmd8).result()
        LOG.info(msg8)
        msg8_list = msg8.split()[0]
        self.assertTrue(float(msg8_list[:-1]) > 0)

    def tearDown(self):
        LOG.info('-----------------清理环境：删除数据库-----------------')
        sql_cmd9 = '''  drop database if exists test; '''
        excute_cmd9 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port} -c "{sql_cmd9}";
            rm -rf  {macro.DB_INSTANCE_PATH}/dump_qm1;
            rm -rf {macro.DB_INSTANCE_PATH}/dump_qm2;  
            rm -rf {macro.DB_INSTANCE_PATH}/dump_qm3;
                     '''
        LOG.info(excute_cmd9)
        msg9 = self.dbuser_node.sh(excute_cmd9).result()
        LOG.info(msg9)
        LOG.info('-----Opengauss_Function_Tools_gs_dump_Case0030finish-----')
