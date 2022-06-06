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
Case Name   : 执行gs_cgroup-c -S {classname} -G {grpname}创建{classname}控制组
              及Workload Cgroups控制组，且默认分配grp为class资源的20%
Description :
    1.omm用户下执行gs_cgroup-c -S {classname} -G {grpname} 创建控制组
    2.gs_cgroup --revert清理环境
Expect      :
    1.创建成功
    2.环境清理成功
History     :
"""
import re
import unittest
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Cgroup_Case0013开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.Class_Name = 'Cgroup_Case0013_class'
        self.Grp_Name = 'Cgroup_Case0013_grp'

    def test_gs_cgroup(self):
        text = '----step1:创建class及workload控制组 expect:创建成功，' \
               'workload资源分配默认为class控制组20%----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
                      f'gs_cgroup -c -S {self.Class_Name} -G {self.Grp_Name};' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        msg1 = msg.split(f'{self.Class_Name}')[1]. \
            split('Workload Group information')[0]
        self.log.info(msg1)
        msg2 = msg.split(f'{self.Grp_Name}')[1]. \
            split('Timeshare Group information')[0]
        self.log.info(msg2)
        assert1 = re.findall('\([0-9]{2}\)', msg1)
        assert2 = re.findall('\([0-9]{2}\)', msg2)
        self.log.info(assert1)
        self.log.info(assert2)
        self.assertIn(self.Class_Name, msg, '执行失败' + text)
        self.assertIn(self.Grp_Name, msg, '执行失败' + text)
        self.assertEqual([f'(20)'], assert1)
        self.assertEqual([f'(20)'], assert2)

    def tearDown(self):
        self.log.info('----step2:清理环境----')
        text = '----gs_cgroup --revert恢复cgroup配置 expect:恢复成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};'\
            f'gs_cgroup --revert'
        msg = self.primary_node.sh(execute_cmd).result()
        self.assertEqual('', msg, '执行失败' + text)
        self.log.info(
            '----Opengauss_Function_Gs_Cgroup_Case0013执行完成----')
