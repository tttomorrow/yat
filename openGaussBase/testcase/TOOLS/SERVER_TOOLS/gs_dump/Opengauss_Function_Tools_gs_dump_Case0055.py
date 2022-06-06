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
Case Name   : 导出的函数体前无美元符号$
Description :
    1.连接数据库
    2.创建数据库test
    3.切换到数据库test
    4.创建函数
    5.退出数据库
    6.source环境变
    7.导出的函数体前无美元符号$
    8.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据库test成功
    3.切换到数据库test
    4.创建表成功
    5.创建视图成功
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
        LOG.info('----opengauss_function_tools_gs_dump_case0055start-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('------------------连接数据库并创建数据库-----------------')
        sql_cmd1 = '''          drop database if exists test;
                                create database test;
                                '''
        excute_cmd1 = f'''     
        source {macro.DB_ENV_PATH} ;
        gsql -d {self.dbuser_node.db_name}\
        -p {self.dbuser_node.db_port} -c "{sql_cmd1}"
                                        '''
        LOG.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg1)
        LOG.info('------------在创建好的数据库中创建函数-------------')
        sql_cmd2 = ''' drop function if exists abort;
                    create function abort(i integer)
                    returns integer
                    as \$$
                    begin
                        return i+1;
                    end;
                    \$$ language plpgsql;
                '''
        excute_cmd2 = f'''source {macro.DB_ENV_PATH} ;
        gsql -d test -p {self.dbuser_node.db_port} -c "{sql_cmd2}"
                                        '''
        LOG.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg2)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, msg2)
        LOG.info('----------------导出的函数体前无美元符号$---------------')
        excute_cmd3 = f'''source {macro.DB_ENV_PATH} ;
         gs_dump -p {self.dbuser_node.db_port} test -F p\
         --disable-dollar-quoting;
                      '''
        LOG.info(excute_cmd3)
        msg3 = self.dbuser_node.sh(excute_cmd3).result()
        LOG.info(msg3)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg3)
        self.assertIn("AS '", msg3)

    def tearDown(self):
        LOG.info('-----------------清理环境：删除数据库-----------------')
        sql_cmd4 = '''  drop database if exists test; '''
        excute_cmd4 = f'''source {macro.DB_ENV_PATH} ;
        gsql -d {self.dbuser_node.db_name}\
        -p {self.dbuser_node.db_port} -c "{sql_cmd4}";
                                       '''
        LOG.info(excute_cmd4)
        msg4 = self.dbuser_node.sh(excute_cmd4).result()
        LOG.info(msg4)
        LOG.info('-----opengauss_function_tools_gs_dump_case0055finish-----')
