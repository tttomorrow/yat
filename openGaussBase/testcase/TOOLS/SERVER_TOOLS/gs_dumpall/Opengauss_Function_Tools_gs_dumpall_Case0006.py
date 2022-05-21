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
Case Name   : gs_dumpall工具指定verbose模式，指定端口号
Description :
    gs_dumpall工具指定verbose模式，指定端口号
Expect      :
    导出成功
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
        LOG.info('---Opengauss_Function_Tools_gs_dumpall_Case0006start---')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        LOG.info('------连接数据库并创建数据库-------')
        sql_cmd1 = '''drop database if exists testdump;
            create database testdump;
            '''
        excute_cmd1 = f'source {macro.DB_ENV_PATH} ;' \
            f'gsql -d {self.dbuser_node.db_name} ' \
            f'-p {self.dbuser_node.db_port} -c "{sql_cmd1}";'
        LOG.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg1)
        LOG.info('--------在创建好的数据库中创建表并插入数据-------')
        sql_cmd2 = '''drop table if exists test1; 
            create table test1 (id int ,name char(10));
            insert into test1 values (1,'aa'),(2,'bb');
            '''
        excute_cmd2 = f'''source {macro.DB_ENV_PATH};
            gsql -d testdump -p {self.dbuser_node.db_port} -c "{sql_cmd2}";
            '''
        LOG.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg2)
        LOG.info('-----指定verbose模式，指定端口号------')
        LOG.info(vars(self.dbuser_node))
        check_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_dumpall --verbose -p {self.dbuser_node.db_port} -l testdump;'
        LOG.info(check_cmd1)
        sql_msg1 = self.dbuser_node.sh(check_cmd1).result()
        LOG.info(sql_msg1)
        self.assertIn(self.constant.gs_dumpall_success_msg, sql_msg1)

    def tearDown(self):
        LOG.info('--------------无需清理环境-------------------')
        LOG.info('--Opengauss_Function_Tools_gs_dumpall_Case0006finish--')
