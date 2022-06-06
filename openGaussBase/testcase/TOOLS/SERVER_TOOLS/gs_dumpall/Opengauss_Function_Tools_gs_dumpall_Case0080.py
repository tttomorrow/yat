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
Case Name   : 导出的数据中对所有标识符加引号，并将结果输出到指定文件
Description :
    1.连接数据库：
    2.创建数据
    3.退出数据库
    4.source环境变量
    5.导出的数据中对所有标识符加引号，并将结果输出到指定文件
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
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0080start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('------------创建数据-------------')
        sql_cmd1 = '''drop table if exists t1; 
            create table t1 (id int ,name char(10));
            insert into t1 values (1,'aa'),(2,'bb');
            '''
        gsql_cmd1 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} -p\
            {self.dbuser_node.db_port} -c "{sql_cmd1}"
            '''
        LOG.info(gsql_cmd1)
        sql_msg1 = self.dbuser_node.sh(gsql_cmd1).result()
        LOG.info(sql_msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_msg1)
        LOG.info('-----导出的数据中对所有标识符加引号，并将结果输出到指定文件-----')
        dumpall_cmd = f'''source {macro.DB_ENV_PATH} ;
            gs_dumpall -p {self.dbuser_node.db_port} --quote-all-identifiers\
            -f {macro.DB_INSTANCE_PATH}/dumpall.sql;
            '''
        LOG.info(dumpall_cmd)
        dumpall_msg = self.dbuser_node.sh(dumpall_cmd).result()
        LOG.info(dumpall_msg)
        self.assertIn(self.constant.gs_dumpall_success_msg, dumpall_msg)
        cat_cmd = f'cat {macro.DB_INSTANCE_PATH}/dumpall.sql;'
        LOG.info(cat_cmd)
        cat_msg = self.dbuser_node.sh(cat_cmd).result()
        LOG.info(cat_msg)
        self.assertIn('CREATE TABLE "t1" ', cat_msg)
        self.assertIn('COPY "t1" ("id", "name") FROM stdin;', cat_msg)

    def tearDown(self):
        LOG.info('----------清理环境----------')
        clear_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port} -c "drop table if exists t1;";
            rm -rf {macro.DB_INSTANCE_PATH}/dumpall.sql;
            '''
        LOG.info(clear_cmd)
        clear_msg = self.dbuser_node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0080finish----')
