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
Case Name   : 指定一个空的主机名称列表文件检查磁盘状态（默认检查当前主机）
Description :
    1.指定一个空的主机名称列表文件检查磁盘状态（默认检查当前主机）
Expect      :
    1.检查信息成功
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
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0036开始-')

        self.log.info("-----创建空的主机列表文件-----")
        touch_cmd = f'touch /home/hostfile ;'
        self.log.info(touch_cmd)
        touch_msg = self.root_user.sh(touch_cmd).result()
        self.log.info(touch_msg)

        self.log.info('---指定一个空的主机名称列表文件检查磁盘状态（默认检查当前主机）---')
        checkos_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkos -i A8 -f /home/hostfile'
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
        rm_cmd = f'rm -rf /home/hostfile'
        self.log.info(rm_cmd)
        rm_msg = self.root_user.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0036结束-')
