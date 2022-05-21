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
Case Name   : gs_cgroup -V 查看gs_cgroup版本
Description :
    1.omm用户下执行gs_cgroup -V  查看系统配置信息
Expect      :
    1.显示gs_cgroup为当前安装版本
History     :
"""
import unittest

from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Cgroup_Case0001开始执行----')
        self.primary_node = Node('PrimaryDbUser')

    def test_gs_cgroup(self):
        text_1 = '----step1:查看gs_cgroup版本 expect:显示正确----'
        self.log.info(text_1)
        version_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_cgroup -V'
        self.log.info(version_cmd)
        msg = self.primary_node.sh(version_cmd).result()
        self.log.info(msg)
        self.assertIn('openGauss', msg, '执行失败' + text_1)

    def tearDown(self):
        self.log.info('----No Need To Clean----')
        self.log.info(
            '----Opengauss_Function_Gs_Cgroup_Case0001执行完成----')
