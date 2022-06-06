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
Case Name   : 执行gs_cgroup-c -S {classname} -s {n%}创建控制组，n取值范围1-99分配控制组资源1-99%
Description :
    1.omm用户下执行gs_cgroup-c -S {classname} -s {n%}创建控制组
    2.gs_cgroup --revert清理环境
Expect      :
    1.创建class控制组成功且分配资源为 n%
    2.环境清理成功
History     :
"""
import re
import unittest
import random

from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Cgroup_Case0007开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.Class_Name = 'Gs_Cgroup_Case0007'

    def test_gs_cgroup(self):
        text = '----step1:创建class控制组 expect:创建成功，分配资源为 n%----'
        self.log.info(text)
        percent = random.randint(1, 99)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
                      f'gs_cgroup -u -S DefaultClass -s 1;' \
                      f'gs_cgroup -c -S {self.Class_Name} -s {percent};' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        msg1 = msg.split(f'{self.Class_Name}')[1]. \
            split('Workload Group information')[0]
        msg2 = msg.split('DefaultClass')[1].split('CLASS')[0]
        self.log.info(msg2)
        assert2 = re.findall('\( [0-9]\)', msg2)
        self.log.info(assert2)
        self.log.info(msg1)
        if percent < 10:
            assert1 = re.findall('\( [0-9]\)', msg1)
            self.assertEqual([f'( {percent})'], assert1)
        else:
            assert1 = re.findall('\([0-9]{2}\)', msg1)
            self.assertEqual([f'({percent})'], assert1)
        self.log.info(assert1)
        self.assertEqual([f'( 1)'], assert2)
        self.assertIn(self.Class_Name, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----step2:清理环境----')
        text = '----gs_cgroup --revert恢复cgroup配置 expect:恢复成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};'\
            f'gs_cgroup --revert'
        msg = self.primary_node.sh(execute_cmd).result()
        self.assertEqual('', msg, '执行失败' + text)
        self.log.info(
            '----Opengauss_Function_Gs_Cgroup_Case0007执行完成----')
