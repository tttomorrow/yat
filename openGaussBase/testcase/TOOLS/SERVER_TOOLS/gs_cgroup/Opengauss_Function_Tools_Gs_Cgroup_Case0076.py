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
Case Name   : 设置Gaussdb控制组cpu核数（a-b）a，b∈[0,max),a<=b
Description :
    1.omm用户下执行gs_cgroup -u -f a-b -T Gaussdb
    设置Gaussdb控制组cpu核数（a-b）a，b∈[0,max),a<=b
    2.清理环境
Expect      :
    1.修改成功
    2.清理成功
History     :
"""
import unittest
import random
import re
import os
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)[:-3]}start-----')
        self.primary_node = Node('PrimaryDbUser')

    def test_gs_cgroup(self):
        text = '-----step1:修改Gaussdb控制组cpu核数范围 expect:修改成功-----'
        self.log.info(text)
        cpu_count_cmd = f'cat /proc/cpuinfo| grep "processor"| wc -l'
        self.log.info(cpu_count_cmd)
        cpu_count_msg = self.primary_node.sh(cpu_count_cmd).result()
        self.log.info(cpu_count_msg)
        local_max = int(cpu_count_msg)
        self.log.info(local_max)
        cpu_max = random.randint(0, local_max - 1)
        cpu_min = random.randint(0, cpu_max)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
                      f'gs_cgroup -u -f {cpu_min}-{cpu_max} -T Gaussdb;' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        msg1 = msg.split('Gaussdb')[1].split('Backend')[0]
        assert1 = re.findall('[0-9]+-[0-9]+', msg1)
        self.assertEqual([f'{cpu_min}-{cpu_max}'], assert1, '执行失败' + text)

    def tearDown(self):
        self.log.info('-----step2:清理环境-----')
        text = '-----gs_cgroup --revert恢复cgroup配置 expect:恢复成功-----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};'\
            f'gs_cgroup --revert'
        msg = self.primary_node.sh(execute_cmd).result()
        self.assertEqual('', msg, '执行失败' + text)
        self.log.info(f'-----{os.path.basename(__file__)[:-3]}end-----')
