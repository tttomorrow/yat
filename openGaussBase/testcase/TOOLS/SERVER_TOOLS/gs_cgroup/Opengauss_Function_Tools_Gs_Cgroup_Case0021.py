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
Case Name   : 执行gs_cgroup -d -S {classname}
              删除{classname}组及附属于其的Workload Cgroup控制组
Description :
    1.omm用户下执行gs_cgroup -c -S {classname} -G {grpname1} -g n 创建控制组
    2.omm用户下执行gs_cgroup -d -S {classname}  删除控制组
Expect      :
    1.创建成功
    2.删除成功
History     :
"""
import unittest
import random
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Cgroup_Case0021开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.Class_Name = 'Cgroup_Case0021_class'
        self.Grp_Name = 'Cgroup_Case0021_grp'

    def test_gs_cgroup(self):
        text = '----step1:创建workload1控制组 expect:创建成功----'
        self.log.info(text)
        percent1 = random.randint(1, 99)
        self.log.info(percent1)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
                      f'gs_cgroup -c -S {self.Class_Name} ' \
                      f'-G {self.Grp_Name} -g {percent1};' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.Grp_Name, msg, '执行失败' + text)
        self.assertIn(self.Class_Name, msg, '执行失败' + text)

        text = '----step2:删除class控制组 expect:删除成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -d -S {self.Class_Name};' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertNotIn(self.Class_Name, msg, '执行失败' + text)
        self.assertNotIn(self.Grp_Name, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----No Need To Clean----')
        self.log.info(
            '----Opengauss_Function_Gs_Cgroup_Case0021执行完成----')
