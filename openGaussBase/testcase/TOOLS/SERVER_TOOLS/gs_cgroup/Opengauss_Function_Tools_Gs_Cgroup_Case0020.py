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
Case Name   : 执行gs_cgroup-c -S {classname} -G {grpname} -g n
              同一class组下各Workload控制组配额之和应小于99%
Description :
    1.omm用户下执行gs_cgroup-c -S {classname} -G {grpname1} -g 50 创建控制组
    2.omm用户下执行gs_cgroup-c -S {classname} -G {grpname2} -g 50 创建控制组
    3.gs_cgroup --revert清理环境
Expect      :
    1.创建成功
    2.创建失败
    3.环境清理成功
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
        self.log.info('----Opengauss_Function_Gs_Cgroup_Case0020开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.Class_Name = 'Cgroup_Case0020_class'
        self.Grp_Name1 = 'Cgroup_Case0020_grp1'
        self.Grp_Name2 = 'Cgroup_Case0020_grp2'

    def test_gs_cgroup(self):
        text = '----step1:创建workload1控制组 expect:创建成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
                      f'gs_cgroup -c -S {self.Class_Name} ' \
                      f'-G {self.Grp_Name1} -g 50;' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.Grp_Name1, msg, '执行失败' + text)

        text = '----step2:创建workload2控制组 expect:创建失败----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -c -S {self.Class_Name} ' \
                      f'-G {self.Grp_Name2} -g 50;' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        error_msg = f'ERROR: there is no more resource for ' \
                    f'new cgroup {self.Grp_Name2}.'
        self.assertIn(error_msg, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----step3:清理环境----')
        text = '----gs_cgroup --revert恢复cgroup配置 expect:恢复成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};'\
            f'gs_cgroup --revert'
        msg = self.primary_node.sh(execute_cmd).result()
        self.assertEqual('', msg, '执行失败' + text)
        self.log.info(
            '----Opengauss_Function_Gs_Cgroup_Case0020执行完成----')
