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
Case Name   : root用户创建用户默认控制组GAUSSHOME_PATH配置错误
Description :
    1.创建omm用户
    2.root用户下执行gs_cgroup -U {username} -H {GAUSSHOME_PATH} -c
    GAUSHOME_PATH错误创建默认控制组
    3.清理环境
Expect      :
    1.创建成功
    2.创建失败
    3.清理成功
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
        self.u_name = 'Cgroup_Case0067'

    def test_gs_cgroup(self):
        text = '----step1创建omm用户: expect:创建成功----'
        self.log.info(text)
        self.common.create_user(self.primary_root_node, self.u_name)
        text = '----step2 GAUSSHOME_PATH配置错误创建控制组: expect:创建失败----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -U {self.u_name} -H ' \
                      f'{macro.DB_INSTANCE_PATH} -c;'
        self.log.info(execute_cmd)
        msg = self.primary_root_node.sh(execute_cmd).result()
        self.log.info(msg)
        error_msg = f'ERROR: failed to create and map the configure file ' \
                    f'{macro.DB_INSTANCE_PATH}/etc/gscgroup_{self.u_name}.' \
                    f'cfg!\nFATAL: failed to parse the configure file!'
        self.assertIn(error_msg, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----step3:清理环境----')
        text = '----删除用户及控制组 expect:恢复成功----'
        self.log.info(text)
        userdel_cmd = f'userdel -r {self.u_name}'
        self.log.info(userdel_cmd)
        del_msg = self.primary_root_node.sh(userdel_cmd).result()
        self.log.info(del_msg)
        count1 = 0
        while del_msg and count1 <= 6:
            assert1 = del_msg.split(' ')[-1]
            self.log.info(assert1)
            kill_msg = self.primary_root_node.\
                sh('kill -9 %s \n' % assert1).result()
            self.log.info(kill_msg)
            del_msg = self.primary_root_node.sh(userdel_cmd).result()
            self.log.info(del_msg)
            count1 += 1
            continue
        self.assertEqual('', del_msg, '执行失败' + text)
        self.log.info(f'----{os.path.basename(__file__)[:-3]}执行完成----')
