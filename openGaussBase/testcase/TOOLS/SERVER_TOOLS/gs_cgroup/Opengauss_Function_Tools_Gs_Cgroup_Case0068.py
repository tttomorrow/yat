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
Case Name   : root用户为已配置omm默认控制组用户创建控制组
Description :
    1.root用户下执行gs_cgroup -U {primarydbuser} -H {GAUSSHOME_PATH} -c
    为已创建默认控制组的primarydbuser用户创建默认控制组
Expect      :
    1.创建失败
History     :
"""
import unittest
import os
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.common = Common()
        self.log.info(f'----{os.path.basename(__file__)[:-3]}开始执行----')
        self.primary_root_node = Node('PrimaryRoot')
        self.primary_node = Node('PrimaryDbUser')
        self.primary_node_name = self.primary_node.ssh_user
        self.log.info(self.primary_node_name)
        self.gausshome_path = \
            os.path.join(os.path.split(macro.DB_INSTANCE_PATH)[0], 'app')

    def test_gs_cgroup(self):
        text = '----step1 root为已创建默认控制组的primarydbuser用户默认控制组: ' \
               'expect:创建失败----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -U {self.primary_node_name} ' \
                      f'-H {self.gausshome_path} -c;'
        self.log.info(execute_cmd)
        msg = self.primary_root_node.sh(execute_cmd).result()
        self.log.info(msg)
        error_msg = f'\'/sys/fs/cgroup/cpu,' \
                    f'cpuacct/CM:{self.primary_node_name}\' ' \
                    f'exists, omit to create this cgroup.'
        self.assertIn(error_msg, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----No Need To Clean----')
        self.log.info(f'----{os.path.basename(__file__)[:-3]}执行完成----')
