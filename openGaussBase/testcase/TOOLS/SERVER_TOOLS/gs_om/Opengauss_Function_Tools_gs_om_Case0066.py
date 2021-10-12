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
Case Name   : 查询数据库状态时，显示指定服务器数据库所有节点信息
Description :
    1.查询数据库状态时，显示指定服务器数据库所有节点信息
    2.查看显示是否正确
Expect      :
    1.查询成功
    2.查看显示正确
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0066start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.logger.info('-----查看主机名称-----')
        check_cmd = f'hostname'
        self.logger.info(check_cmd)
        hostname = self.dbuser_node.sh(check_cmd).result()
        self.logger.info(hostname)
        self.logger.info('------查询数据库状态时，显示指定服务器数据库所有节点信息-------')
        om_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_om ' \
            f'-t status ' \
            f'-h {hostname} ' \
            f'--all ; '
        self.logger.info(om_cmd1)
        om_msg1 = self.dbuser_node.sh(om_cmd1).result()
        self.logger.info(om_msg1)
        self.assertIn('cluster_state',  om_msg1)

    def tearDown(self):
        self.logger.info('--------------无需清理环境-------------------')
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0066finish--')
