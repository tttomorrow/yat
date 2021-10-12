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
Case Name   : 检查主机磁盘状态，将OS检查报告输出到指定的文件
Description :
    1.检查主机磁盘状态，将OS检查报告输出到指定的文件
    2.查看文件信息，分析检查结果
Expect      :
    1.检查磁盘状态成功，状态信息输出到指定文件
    2.查看文件信息成功，检查结果正常
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
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0051开始-')

        self.log.info('--------检查主机磁盘状态，将OS检查报告输出到指定的文件---------')
        checkos_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkos -i A8 -o /home/osfile/osfile.log;' \
            f'gs_checkos -i A8 -o /home/osfile/osfile.txt;'
        self.log.info(checkos_cmd)
        checkos_msg = self.root_user.sh(checkos_cmd).result()
        self.log.info(checkos_msg)
        self.assertIn('Operation system check/set is completed', checkos_msg)

        self.log.info('---------------查看文件信息，分析检查结果-----------------')

        checkos_cmd = f'cat /home/osfile/osfile.log'
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

        checkos_cmd = f'cat /home/osfile/osfile.txt'
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
        rm_cmd = f'rm -rf /home/osfile'
        self.log.info(rm_cmd)
        rm_msg = self.root_user.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0051结束-')
