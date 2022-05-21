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
Case Name   : root用户为不存在omm用户创建默认控制组
Description :
    1.root用户下执行gs_cgroup -U {username} -H {GAUSSHOME_PATH} -c 创建默认控制组
Expect      :
    1.创建失败
History     :
"""
import unittest
import os
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)[:-3]}开始执行----')
        self.primary_root_node = Node('PrimaryRoot')
        self.primary_node = Node('PrimaryDbUser')
        self.u_name = 'Cgroup_Case0066'
        self.gausshome_path = \
            os.path.join(os.path.split(macro.DB_INSTANCE_PATH)[0], 'app')

    def test_gs_cgroup(self):
        text = '----step1 root下为不存在omm用户创建默认控制组: expect:创建失败----'
        self.log.info(text)
        userdel_cmd = f'userdel -r {self.u_name}'
        self.log.info(userdel_cmd)
        self.primary_root_node.sh(userdel_cmd)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -U {self.u_name} -H {self.gausshome_path} -c;'
        self.log.info(execute_cmd)
        msg = self.primary_root_node.sh(execute_cmd).result()
        self.log.info(msg)
        error_msg = f'ERROR: can\'t get the uid and gid of {self.u_name}.'
        self.assertIn(error_msg, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----No Need To Clean----')
        self.log.info(f'----{os.path.basename(__file__)[:-3]}执行完成----')
