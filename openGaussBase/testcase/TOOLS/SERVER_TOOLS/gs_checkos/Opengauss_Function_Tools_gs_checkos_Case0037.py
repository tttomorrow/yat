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
Case Name   : 指定主机名称列表文件，但不使用参数i，检查主机信息
Description :
    1.指定主机名称列表文件，但不使用参数i，检查主机信息
Expect      :
    1.信息检查失败
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.primary_dbuser = Node('PrimaryDbUser')
        self.root_user = Node('default')

    def test_server_tools1(self):
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0037开始-')
        self.error_msg = 'Incorrect parameter. Parameter \'-i\' is required'

        self.log.info('-----查看主机名称-----')
        check_cmd = f'hostname'
        self.log.info(check_cmd)
        hostname = self.primary_dbuser.sh(check_cmd).result()
        self.log.info(hostname)

        self.log.info('-----将主机名写入列表文件-----')
        echo_cmd = f'echo \'{hostname}\' > /home/hostfile.txt'
        self.log.info(echo_cmd)
        echo_msg = self.root_user.sh(echo_cmd).result()
        self.log.info(echo_msg)

        self.log.info('---指定主机名称列表文件，但不使用参数i，检查主机信息---')
        checkos_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkos  -f /home/hostfile.txt'
        self.log.info(checkos_cmd)
        checkos_msg = self.root_user.sh(checkos_cmd).result()
        self.log.info(checkos_msg)
        self.assertIn(self.error_msg, checkos_msg)

    def tearDown(self):
        self.log.info('-----------------清理环境----------------')
        rm_cmd = f'rm -rf /home/hostfile.txt'
        self.log.info(rm_cmd)
        rm_msg = self.root_user.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0037结束-')
