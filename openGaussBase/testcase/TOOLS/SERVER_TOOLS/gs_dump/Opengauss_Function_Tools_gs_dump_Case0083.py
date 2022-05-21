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
Case Name   : 使用初始用户连接数据，不指定用户名和密码
Description :
    1.只使用主机名和端口连接
    2.使用主机名和端口连接指定的数据库
Expect      :
    1.连接失败
    2.连接失败
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
        LOG.info('----Opengauss_Function_Tools_gs_dump_Case0083start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('------------------显示帮助信息------------------')
        LOG.info('-----只使用主机名和端口连接-----')
        excute_cmd1 = f'''source {macro.DB_ENV_PATH} ;
        gs_dump -h {self.dbuser_node.db_host} -p {self.dbuser_node.db_port};
                              '''
        LOG.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn('failed', msg1)
        LOG.info('-----指定连接的数据库连接-----')
        excute_cmd2 = f'''source {macro.DB_ENV_PATH} ;
                        gs_dump -h {self.dbuser_node.db_host} -p\
        {self.dbuser_node.db_port}  {self.dbuser_node.db_name};
                                      '''
        LOG.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg2)
        self.assertIn('failed', msg2)

    def tearDown(self):
        LOG.info('--------------无需清理环境-------------------')
        LOG.info('----Opengauss_Function_Tools_gs_dump_Case0083finish-----')
