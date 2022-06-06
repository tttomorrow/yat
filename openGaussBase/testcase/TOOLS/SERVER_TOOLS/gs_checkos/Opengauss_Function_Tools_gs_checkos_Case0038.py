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
Case Name   : 指定主机名称列表文件，检查磁盘配置状态
Description :
    1.将主机、备机名写入列表文件
    2.root用户检查机器磁盘配置信息
    3.清理环境
Expect      :
    1.将主机备机名写入列表文件
    2.root用户检查机器磁盘配置信息
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
        self.primary_dbuser = Node('PrimaryDbUser')
        self.root_user = Node('default')

    def test_server_tools1(self):
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0038开始-')
        self.log.info('----若为单机环境，后续不执行，直接通过----')
        excute_cmd = f' source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail;'
        self.log.info(excute_cmd)
        msg = self.primary_dbuser.sh(excute_cmd).result()
        self.log.info(msg)
        if 'Standby' not in msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.standby1_dbuser = Node('Standby1DbUser')

        self.log.info('-----查看主机名称-----')
        check_cmd = f'hostname'
        self.log.info(check_cmd)
        hostname1 = self.primary_dbuser.sh(check_cmd).result()
        self.log.info(hostname1)

        self.log.info('-----查看备机名称-----')
        check_cmd = f'hostname'
        self.log.info(check_cmd)
        hostname2 = self.standby1_dbuser.sh(check_cmd).result()
        self.log.info(hostname2)

        self.log.info('-----将主机、备机名写入列表文件-----')
        echo_cmd = f'echo \'{hostname1}\' , \'{hostname2}\'' \
            f'> /home/hostfile.txt'
        self.log.info(echo_cmd)
        msg = self.root_user.sh(echo_cmd).result()
        self.log.info(msg)

        self.log.info('---指定主机名称列表文件，检查磁盘配置状态---')
        checkos_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkos -i A8 -f /home/hostfile.txt'
        self.log.info(checkos_cmd)
        checkos_msg = self.root_user.sh(checkos_cmd).result()
        self.log.info(checkos_msg)
        list1 = checkos_msg.split('\n')
        self.log.info(list1)
        list2 = list1[1].split(':')
        self.log.info(list2)
        self.assertEqual(list2[0].strip(),
            'A8. [ Disk configuration status ]', '状态异常')
        i = list2[1].strip()
        self.assertTrue(i in ['Normal', 'Warning'], f'状态异常: {i}')

    def tearDown(self):
        self.log.info('-----------------清理环境----------------')
        rm_cmd = f'rm -rf /home/hostfile.txt'
        self.log.info(rm_cmd)
        rm_msg = self.root_user.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0038结束-')
