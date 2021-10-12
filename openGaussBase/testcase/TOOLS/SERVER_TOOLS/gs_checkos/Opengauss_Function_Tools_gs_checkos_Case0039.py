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
Case Name   : 指定主机名称列表文件，文件中主机名称有误，检查磁盘状态
Description :
    1.将错误主机名写入列表文件
    2.root用户检查主机磁盘状态
    3.清理环境
Expect      :
    1.将错误主机名写入列表文件成功
    2.root用户检查主机磁盘信息失败
    3.清理环境成功
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

    def test_server_tools1(self):
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0039开始-')
        self.log.info('-----将错误主机名写入列表文件-----')
        echo_cmd = f'echo \'ctupddl0000\' > /home/hostfile.txt'
        self.log.info(echo_cmd)
        msg = self.root_user.sh(echo_cmd).result()
        self.log.info(msg)

        self.log.info('-指定主机名称列表文件，文件中主机名称有误，检查磁盘状态-')
        checkos_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkos -i A8 -f /home/hostfile.txt'
        self.log.info(checkos_cmd)
        checkos_msg = self.root_user.sh(checkos_cmd).result()
        self.log.info(checkos_msg)
        self.assertIn('Check_Disk_Configure -l '
            '\'/tmp/gs_checkos/gs_local.log\' . Error', checkos_msg)

    def tearDown(self):
        self.log.info('-----------------清理环境----------------')
        rm_cmd = f'rm -rf /home/hostfile.txt'
        self.log.info(rm_cmd)
        rm_msg = self.root_user.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0039结束-')
