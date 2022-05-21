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
Case Name   : 所属Backend组下各backend控制组配额之和应小于等于100%
Description :
    1.omm用户下执行gs_cgroup -u -B {backendname} -b {n}
    修改Backend组下控制组资源分配之和大于等于100%
    2.清理环境
Expect      :
    1.修改失败
    2.清理成功
History     :
"""
import unittest
import re
import os
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)[:-3]}开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.Back_grp_lis = ['DefaultBackend', 'Vacuum']

    def test_gs_cgroup(self):
        text = '----step1:修改Backend组下控制组资源分配之和大于等于100%' \
               ' expect:修改失败----'
        self.log.info(text)
        for grp_name in self.Back_grp_lis:
            execute_cmd = f'source {macro.DB_ENV_PATH};' \
                          f'gs_cgroup --revert;' \
                          f'gs_cgroup -u -B {grp_name} -b 50;' \
                          f'gs_cgroup -p'
            self.log.info(execute_cmd)
            msg = self.primary_node.sh(execute_cmd).result()
            self.log.info(msg)
            if grp_name == 'DefaultBackend':
                msg1 = msg.split('Backend Group '
                                 'information is listed:')[1].split('Vacuum')[0]
                assert1 = re.findall('\(\s*[0-9]{2}\)', msg1)
                self.assertEqual([f'(50)'], assert1, '执行失败' + text)
            else:
                error_msg = f'ERROR: there is no more resource for ' \
                            f'updated cgroup {grp_name}.'
                self.assertIn(error_msg, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----step2:清理环境----')
        text = '----gs_cgroup --revert恢复cgroup配置 expect:恢复成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};'\
            f'gs_cgroup --revert'
        msg = self.primary_node.sh(execute_cmd).result()
        self.assertEqual('', msg, '执行失败' + text)
        self.log.info(f'----{os.path.basename(__file__)[:-3]}执行完成----')
