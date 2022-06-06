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
Case Name   : 检查配置文件中参数，不指定参数名称-c
Description :
    1.检查指定主机的指定实例路径时不指定检查参数
    2.检查所有主机的所有实例路径时不指定检查参数
Expect      :
    1.执行失败
    2.执行失败
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0008开始执行-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        LOG.info('------检查指定主机的指定实例路径时不指定检查参数------')
        check_cmd = f'''hostname'''
        LOG.info(check_cmd)
        hostname = self.dbuser_node.sh(check_cmd).result()
        excute_cmd2 = f'''
                source {macro.DB_ENV_PATH}
                gs_guc check -N {hostname} -D {macro.DB_INSTANCE_PATH}
                '''
        LOG.info(excute_cmd2)
        msg1 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg1)
        self.assertIn('gs_guc: the form of this command is incorrect', msg1)
        LOG.info('------检查所有主机的所有实例路径------')
        excute_cmd2 = f'''
                               source {macro.DB_ENV_PATH}
                               gs_guc check  -N all  -I all '''
        LOG.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        self.assertIn('gs_guc: the form of this command is incorrect', msg2)

    def tearDown(self):
        LOG.info('----------------无需清理环境-----------------------')
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0008执行结束-----')
