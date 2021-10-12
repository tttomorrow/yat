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
Case Name   : 检查操作系统版本时显示检查结果详情
Description :
    1.检查操作系统版本时显示检查结果详情
Expect      :
    1.检查操作系统版本时显示检查结果详情成功
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
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0050开始-')
        self.log.info('---查看linux操作系统位数---')
        bit_cmd = f'getconf LONG_BIT'
        self.log.info(bit_cmd)
        bit_msg = self.root_user.sh(bit_cmd).result()
        self.log.info(bit_msg)
        self.log.info('---查看linux操作系统版本信息---')
        cat_cmd = f'cat /etc/system-release'
        self.log.info(cat_cmd)
        cat_msg = self.root_user.sh(cat_cmd).result()
        self.log.info(cat_msg)
        self.log.info('---步骤1 检查操作系统版本时显示检查结果详情---')
        checkos_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkos -i A1 --detail'
        self.log.info(checkos_cmd)
        checkos_msg = self.root_user.sh(checkos_cmd).result()
        self.log.info(checkos_msg)
        self.log.info('---预处理checkos方法获取的信息---')
        checkos_list1 = checkos_msg.split('\n')
        self.log.info(checkos_list1)
        checkos_list2 = checkos_list1[3].split('_')
        self.log.info(checkos_list2)
        self.log.info('---获取checkos方法得到操作系统信息---')
        version_a2 = checkos_list2[0].strip()
        self.log.info(version_a2)
        self.log.info('---获取checkos方法得到操作系统版本号---')
        num_a2 = checkos_list2[1]
        self.log.info(num_a2)
        self.log.info('---CentOS系统和openEuler系统cat返回信息不同，所以校验方法略有不同---')
        if 'CentOS' in cat_msg:
            cat_list = cat_msg.split(' ')
            self.log.info(cat_list)
            self.log.info('---处理cat方法获取的系统信息---')
            version_a1 = cat_list[0].lower()
            self.log.info(version_a1)
            self.log.info('---处理cat方法获取的操作系统版本号---')
            num_a1 = cat_list[3]
            self.log.info(num_a1)
            self.assertEqual(version_a1, version_a2)
            self.assertEqual(num_a1, num_a2)
            self.assertIn(bit_msg, checkos_list2[2])
        elif 'openEuler' in cat_msg:
            cat_list = cat_msg.split(' ')
            self.log.info(cat_list)
            self.log.info('---处理cat方法获取的系统信息---')
            version_a1 = cat_list[0]
            self.log.info(version_a1)
            self.log.info('---处理cat方法获取的操作系统版本号---')
            num_a1 = cat_list[2]
            self.log.info(num_a1)
            self.assertEqual(version_a1, version_a2)
            self.assertEqual(num_a1, num_a2)
            self.assertIn(bit_msg, checkos_list2[2])

    def tearDown(self):
        self.log.info('-----------------无需清理环境----------------')
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0050结束-')
