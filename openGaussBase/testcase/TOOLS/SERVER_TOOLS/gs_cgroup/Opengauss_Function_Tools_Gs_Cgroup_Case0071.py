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
Case Name   : 更改Class下的自定义{classname}组cpu占用比例n!=[0,100]
Description :
    1.omm用户下执行gs_cgroup -c -S {classname} -G {grpname1}
    创建class及workload控制组
    2.omm用户下执行gs_cgroup -u --fixed -S {classname} -s n
    配置Class组下{classname}控制组资源分配为n%，n!=[0,100]
    3.gs_cgroup --revert清理环境
Expect      :
    1.创建成功
    2.修改失败
    3.环境清理成功
History     :
"""
import unittest
import random
import os
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)[:-3]}开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.Class_Name = 'Cgroup_Case0071_class'
        self.Grp_Name = 'Cgroup_Case0071_grp'

    def test_gs_cgroup(self):
        text = '----step1:创建class及workload控制组 expect:创建成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
                      f'gs_cgroup -c -S {self.Class_Name} -G {self.Grp_Name};' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.Class_Name, msg, '执行失败' + text)
        self.assertIn(self.Grp_Name, msg, '执行失败' + text)

        text = '----step2:更改class组cpu核数使用范围!=[0,100]uint型 ' \
               'expect:修改失败----'
        self.log.info(text)
        percent1 = random.randint(101, 65535)
        percent2 = random.randint(-65535, -1)
        percent_lis = [percent1, percent2]
        for percent in percent_lis:
            execute_cmd = f'source {macro.DB_ENV_PATH};' \
                          f'gs_cgroup -u --fixed -S {self.Class_Name} -s ' \
                          f'{percent};' \
                          f'gs_cgroup -p'
            self.log.info(execute_cmd)
            msg = self.primary_node.sh(execute_cmd).result()
            self.log.info(msg)
            error_msg = 'ERROR: invalid value for cpu core percentage. ' \
                        'its range should be 0-100.'
            self.assertIn(error_msg, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----step3:清理环境----')
        text = '----gs_cgroup --revert恢复cgroup配置 expect:恢复成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};'\
            f'gs_cgroup --revert'
        msg = self.primary_node.sh(execute_cmd).result()
        self.assertEqual('', msg, '执行失败' + text)
        self.log.info(f'----{os.path.basename(__file__)[:-3]}执行完成----')
