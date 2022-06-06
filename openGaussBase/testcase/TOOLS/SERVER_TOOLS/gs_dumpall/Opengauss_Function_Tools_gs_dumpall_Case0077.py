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
Case Name   : 导出的数据去掉函数体前面的$符,并将数据导入指定的文件
Description :
    1.连接数据库：
    2.创建数据
    3.退出数据库
    4.source环境变量
    5.导出的数据去掉函数体前面的$符,并将数据导入指定的文件
    6.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据成功
    3.退出数据库
    4.source环境变量
    5.导出的数据去掉函数体前面的$符,并将数据导入指定的文件成功
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
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0077start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('------------创建函数-------------')
        sql_cmd1 = '''drop function if exists abort;
            create function abort(i integer)
            returns integer
            as \$$
            begin
                return i+1;
            end;
            \$$ language plpgsql;
            '''
        gsql_cmd1 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} -p\
            {self.dbuser_node.db_port} -c "{sql_cmd1}";
            '''
        LOG.info(gsql_cmd1)
        sql_msg1 = self.dbuser_node.sh(gsql_cmd1).result()
        LOG.info(sql_msg1)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, sql_msg1)

        LOG.info('------导出的数据去掉函数体前面的$符,并将数据导入指定的文件-----')
        dumpall_cmd = f'''source {macro.DB_ENV_PATH} ;
            gs_dumpall -p {self.dbuser_node.db_port} \
            --disable-dollar-quoting\
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
        self.assertIn("AS '", cat_msg)

    def tearDown(self):
        LOG.info('---清理环境---')
        sql_cmd2 = 'drop function if exists abort;'
        clear_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}\
            -p {self.dbuser_node.db_port} -c "{sql_cmd2}";
            rm -rf {macro.DB_INSTANCE_PATH}/dumpall.sql;
            '''
        LOG.info(clear_cmd)
        clear_msg = self.dbuser_node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0077finish----')
