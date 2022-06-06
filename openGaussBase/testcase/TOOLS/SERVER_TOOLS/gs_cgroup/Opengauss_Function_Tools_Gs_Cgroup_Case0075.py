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
Case Name   : 设置Gaussdb控制组cpu核数（a）a！=[0,max),max为本机最大核数
Description :
    1.omm用户下执行gs_cgroup -u -f a -T Gaussdb
    设置Gaussdb控制组cpu核数（a）a！=[0,max),max为本机最大核数
Expect      :
    1.修改失败
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
        self.log.info(f'-----{os.path.basename(__file__)[:-3]}start-----')
        self.primary_node = Node('PrimaryDbUser')

    def test_gs_cgroup(self):
        text = '-----step1:修改gaussdb的cpu核数使用范围 expect:修改失败-----'
        self.log.info(text)
        cpu_count_cmd = f'cat /proc/cpuinfo| grep "processor"| wc -l'
        self.log.info(cpu_count_cmd)
        cpu_count_msg = self.primary_node.sh(cpu_count_cmd).result()
        self.log.info(cpu_count_msg)
        local_max = int(cpu_count_msg)
        self.log.info(local_max)
        cpu_max_lis = [local_max, random.randint(local_max + 1, 65535)]
        for cpu_max in cpu_max_lis:
            execute_cmd = f'source {macro.DB_ENV_PATH};' \
                          f'gs_cgroup --revert;' \
                          f'gs_cgroup -u -f {cpu_max} -T Gaussdb;' \
                          f'gs_cgroup -p'
            self.log.info(execute_cmd)
            msg = self.primary_node.sh(execute_cmd).result()
            self.log.info(msg)
            error_msg = f'ERROR: please specify the cpuset with a valid value.'
            self.assertIn(error_msg, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('-----No Need To Clean-----')
        self.log.info(f'-----{os.path.basename(__file__)[:-3]}end-----')
