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
Case Name   : 数据库关闭时，一次指定多个服务器
Description :
    1.查看数据库状态：gs_om -t status --detail
    2.关闭数据库时指定多个服务器是否可以关闭成功
    3.查看数据库状态：gs_om -t status --detail
Expect      :
    1.状态正常
    2.执行失败
    3.状态正常
History     : 
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Tools_gs_om_Case0040start---')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.log.info('-----------------查看数据库状态-------------------')
        status_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail ;'
        self.log.info(status_cmd)
        status_msg = self.dbuser_node.sh(status_cmd).result()
        self.log.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)
        if 'Standby' not in status_msg:
            self.log.info('---单机环境，后续不执行，直接通过---')
        else:
            self.standby_node = Node('Standby1DbUser')
            self.log.info('-----查看主机名称-----')
            check_cmd = f'hostname'
            self.log.info(check_cmd)
            hostname1 = self.dbuser_node.sh(check_cmd).result()
            self.log.info(hostname1)

            self.log.info('-----查看备机名称-----')
            check_cmd = f'hostname'
            self.log.info(check_cmd)
            hostname2 = self.standby_node.sh(check_cmd).result()
            self.log.info(hostname2)

            self.log.info('----------数据库关闭时，指定多个服务器名称值----------')
            certificate_path = os.path.join(macro.DB_INSTANCE_PATH, 'server.*')
            ls_cmd = f'ls -l {certificate_path}'
            self.log.info(ls_cmd)
            stop_cmd = f'source {macro.DB_ENV_PATH}; ' \
                f'gs_om -t stop -h {hostname1},{hostname2};'
            self.log.info(stop_cmd)
            stop_msg = self.dbuser_node.sh(stop_cmd).result()
            self.log.info(stop_msg)
            self.assertIn('Too many command-line arguments', stop_msg)

            self.log.info('-----------------查看数据库状态-------------------')
            status_cmd = f'source {macro.DB_ENV_PATH};' \
                f'gs_om -t status --detail ;'
            self.log.info(status_cmd)
            status_msg = self.dbuser_node.sh(status_cmd).result()
            self.log.info(status_msg)
            self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)

    def tearDown(self):
        self.log.info('------------无需清理环境-------------')
        self.log.info('--Opengauss_Function_Tools_gs_om_Case0040finish--')
