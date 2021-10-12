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
Case Name   : 查询指定服务器状态的详细信息（-detail,--all）
Description :
    1.查询指定服务器状态的详细信息（-detail,--all）
    2.查看信息显示是否正常
Expect      :
    1.查询成功
    2.查看信息显示正常
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
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0077start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.logger.info('------查询指定服务器状态的详细信息（-detail,--all）-------')
        self.logger.info('------------查看主机名称-------------')
        check_cmd = f'hostname'
        self.logger.info(check_cmd)
        hostname = self.dbuser_node.sh(check_cmd).result()
        self.logger.info(hostname)
        om_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_om ' \
            f'-t status ' \
            f'-h {hostname} ' \
            f'--detail  ' \
            f'--all'
        self.logger.info(om_cmd1)
        om_msg1 = self.dbuser_node.sh(om_cmd1).result()
        self.logger.info(om_msg1)
        self.assertIn('Cluster State', om_msg1)
        self.assertIn('Datanode State', om_msg1)

    def tearDown(self):
        self.logger.info('--------------无需清理环境-------------------')
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0077finish--')
