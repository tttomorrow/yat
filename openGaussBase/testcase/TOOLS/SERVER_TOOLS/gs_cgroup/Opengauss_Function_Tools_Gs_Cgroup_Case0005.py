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
Case Name   : gs_cgroup -P 以树状查看控制组状态
Description :
    1.omm用户下执行gs_cgroup -P  查看控制组配置参数
Expect      :
    1.配置信息显示正常
History     :
"""
import unittest

from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Cgroup_Case0005开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.assert_lis = ['Mount Information:',
                           'Group Tree Information:']

    def test_gs_cgroup(self):
        text = '----step1:以树状查看控制组配置 expect:信息显示正确----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_cgroup -P'
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        for assert_info in self.assert_lis:
            self.assertIn(assert_info, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----No Need To Clean----')
        self.log.info(
            '----Opengauss_Function_Gs_Cgroup_Case0005执行完成----')
