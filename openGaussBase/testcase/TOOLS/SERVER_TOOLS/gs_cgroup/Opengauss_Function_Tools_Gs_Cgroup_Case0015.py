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
Case Name   : 执行gs_cgroup-c -S {classname} -G {grpname}
              {grpname}中带有':'特殊符号
Description :
    1.omm用户下执行gs_cgroup-c -S {classname} -G {grpname} 创建控制组
Expect      :
    1.创建失败
History     :
"""
import unittest
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Cgroup_Case0015开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.Class_Name = 'Cgroup_Case0015_class'
        self.Grp_Name = 'Cgroup_Case0015_grp:'

    def test_gs_cgroup(self):
        text = '----step1:创建class及workload控制组 expect:创建失败----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
                      f'gs_cgroup -c -S {self.Class_Name} -G {self.Grp_Name};' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        error_msg = f'ERROR, workload group cannot be named with \':\'.'
        self.assertIn(error_msg, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----No Need To Clean----')
        self.log.info(
            '----Opengauss_Function_Gs_Cgroup_Case0015执行完成----')
