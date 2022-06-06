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
Case Name   : 指定需要检查的主机名称的同时指定主机名称文件列表
Description :
    1.指定需要检查的主机名称的同时指定主机名称文件列
Expect      :
    1.检查失败，提示-h和-f不能同时使用
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.root_user = Node('default')
        self.primary_dbuser = Node('PrimaryDbUser')

    def test_server_tools1(self):
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0057开始-')
        self.log.info('-----查看主机名称-----')
        check_cmd = f'hostname'
        self.log.info(check_cmd)
        hostname = self.primary_dbuser.sh(check_cmd).result()
        self.log.info(hostname)

        self.log.info('-----创建hostfile文件-----')
        echo_cmd = f'touch /home/hostfile'
        self.log.info(echo_cmd)
        echo_msg = self.root_user.sh(echo_cmd).result()
        self.log.info(echo_msg)

        self.log.info('----------指定需要检查的主机名称的同时指定主机名称文件列表------------')
        checkos_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkos -i A8 -f /home/hostfile  -h {hostname}'
        self.log.info(checkos_cmd)
        checkos_msg = self.root_user.sh(checkos_cmd).result()
        self.log.info(checkos_msg)
        self.assertIn(f'The parameter \'-h\' and \'-f\' '
            f'can not be used together', checkos_msg)

    def tearDown(self):
        self.log.info('-----------------清理环境----------------')
        rm_cmd = f'rm -rf /home/hostfile'
        self.log.info(rm_cmd)
        rm_msg = self.root_user.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0057结束-')
