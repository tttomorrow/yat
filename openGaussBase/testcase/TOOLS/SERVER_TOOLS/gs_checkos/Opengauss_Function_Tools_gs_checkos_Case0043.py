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
Case Name   : 指定多个需要检查的主机名称（无主备关系），主机之间使用“中文逗号”分割
Description :
    1.指定多个需要检查的主机名称（无主备关系），主机之间使用“中文逗号”分割，检查磁盘配置状态
Expect      :
    2.无主备关系的磁盘配置状态检查失败
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
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0043开始-')

        self.log.info('-----查看主机名称-----')
        check_cmd = f'hostname'
        self.log.info(check_cmd)
        hostname1 = self.primary_dbuser.sh(check_cmd).result()
        self.log.info(hostname1)

        self.log.info('-指定多个需要检查的主机名称（无主备关系），主机之间使用“中文逗号”分割-')
        checkos_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkos -i A8 -h {hostname1}，ctupopenga00009'
        self.log.info(checkos_cmd)
        checkos_msg = self.root_user.sh(checkos_cmd).result()
        self.log.info(checkos_msg)
        self.assertIn('Check_Disk_Configure -l \'/tmp/gs_checkos'
            '/gs_local.log\' . Error', checkos_msg)

    def tearDown(self):
        self.log.info('--------------无需清理环境--------------')
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0043结束-')
