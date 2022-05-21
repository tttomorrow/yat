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
Case Name   : root用户挂载cgroup
Description :
    1.root用户下执行gs_cgroup -M  卸载cgroup控制组
    2.root用户下执行gs_cgroup -m 挂载cgroup控制组
Expect      :
    1.卸载成功
    2.挂载成功
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
        self.assert_lis = ['Top Group information is listed:',
                           'Backend Group information is listed:',
                           'Class Group information is listed:',
                           'Workload Group information is listed:',
                           'Timeshare Group information is listed:',
                           'Group Exception information is listed:']

    def test_gs_cgroup(self):
        text = '----step1卸载cgroup控制组: expect:卸载成功----'
        self.log.info(text)
        unmount_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -M;'
        check_cmd = f'source {macro.DB_ENV_PATH};' \
                    f'gs_cgroup -p;'
        check_msg = 'ERROR: failed to add cpu controller in 0!\nERROR: ' \
                    'failed to get cpusets and mems during initialization.'
        self.log.info(unmount_cmd)
        self.log.info(check_cmd)
        msg = self.primary_root_node.sh(unmount_cmd).result()
        self.log.info(msg)
        msg1 = self.primary_node.sh(check_cmd).result()
        self.log.info(msg1)
        self.assertIn(check_msg, msg1, '执行失败' + text)

        text = '----step2挂载cgroup控制组: expect:挂载成功----'
        self.log.info(text)
        mount_cmd = f'source {macro.DB_ENV_PATH};' \
                    f'gs_cgroup -m;'
        check_cmd = f'source {macro.DB_ENV_PATH};' \
                    f'gs_cgroup -p;'
        self.log.info(mount_cmd)
        self.log.info(check_cmd)
        msg = self.primary_root_node.sh(mount_cmd).result()
        self.log.info(msg)
        msg1 = self.primary_node.sh(check_cmd).result()
        self.log.info(msg1)
        for assert_info in self.assert_lis:
            self.assertIn(assert_info, msg1, '执行失败' + text)

    def tearDown(self):
        self.log.info('----No Need To Clean----')
        self.log.info(f'----{os.path.basename(__file__)[:-3]}执行完成----')
