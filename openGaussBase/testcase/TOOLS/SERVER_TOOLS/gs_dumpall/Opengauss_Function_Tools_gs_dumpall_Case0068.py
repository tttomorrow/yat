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
Case Name   : root用户执行gs_dumpall工具
Description :
    1.连接数据库：
    2.创建数据
    3.退出数据库
    4.source环境变量
    5.root用户执行gs_dumpall工具
    6.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据成功
    3.退出数据库
    4.source环境变量
    5.导出失败
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
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0068start----')
        self.dbuser_node = Node('dbuser')
        self.root_node = Node('default')
        self.constant = Constant()
        self.dumpall_error_msg = 'Invalid username/password,login denied'

    def test_server_tools(self):
        LOG.info('------------创建数据-------------')
        sql_cmd1 = '''drop table if exists test1; 
            create table test1 (id int ,name char(10));
            insert into test1 values (1,'aa'),(2,'bb');
            '''
        gsql_cmd1 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} -p\
            {self.dbuser_node.db_port} -c "{sql_cmd1}";
            '''
        LOG.info(gsql_cmd1)
        sql_msg1 = self.dbuser_node.sh(gsql_cmd1).result()
        LOG.info(sql_msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_msg1)
        gsql_cmd2 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} -p\
            {self.dbuser_node.db_port} -c "\\l";
            '''
        LOG.info(gsql_cmd2)
        sql_msg2 = self.dbuser_node.sh(gsql_cmd2).result()
        LOG.info(sql_msg2)
        end_line = sql_msg2.splitlines()[-1].strip()
        LOG.info(end_line)
        db_num = end_line.split()[0].strip('(')
        LOG.info(db_num)

        LOG.info('--root用户执行gs_dumpall工具--')
        self.var = f'''expect "Password:"
            send "{self.root_node.ssh_password}\\n"
            '''
        dumpall_cmd = f'''source {macro.DB_ENV_PATH};
            expect <<EOF
            set timeout -1
            spawn gs_dumpall -p {self.root_node.db_port}
            {self.var * (int(db_num)-2)}
            expect eof \n''' + "EOF"
        LOG.info(dumpall_cmd)
        dumpall_msg = self.root_node.sh(dumpall_cmd).result()
        LOG.info(dumpall_msg)
        self.assertIn(self.dumpall_error_msg, dumpall_msg)

    def tearDown(self):
        LOG.info('---清理环境---')
        sql_cmd2 = 'drop table if exists test1;'
        clear_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port} -c "{sql_cmd2}";
            '''
        LOG.info(clear_cmd)
        clear_msg = self.dbuser_node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0068finish----')
