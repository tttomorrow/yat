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
Case Name   : 设置CPUSkewPercent,QualificationTime指定--penalty后指定异常操作为--a
Description :
    1.omm用户下执行gs_cgroup -c -S {classname} -G {grpname1}
    创建class及workload控制组
    2.omm用户下执行gs_cgroup -S {classname} -E "QualificationTime={1-4294967295},
    CPUSkewPercent={1-100}" --penalty   配置参数QualificationTime，cpuskewpercnt
    指定异常操作--penalty
    3.omm用户下执行gs_cgroup -S {classname} -E "QualificationTime={1-4294967295},
    CPUSkewPercent={1-100}" --a   配置参数QualificationTime，cpuskewpercnt
    指定异常操作--a
    4.gs_cgroup --revert清理环境
Expect      :
    1.创建成功
    2.修改成功
    3.修改成功
    4.环境清理成功
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
        self.Class_Name = 'Cgroup_Case0080_class'
        self.Grp_Name = 'Cgroup_Case0080_grp'

    def test_gs_cgroup(self):
        text = '-----step1:创建class及workload控制组 expect:创建成功-----'
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

        text = '-----step2:设置CPUSkewPercent为1-100的unint型，且设置' \
               'QualificationTime为1-4294967295的uint型，' \
               '指定异常操作penalty  expect:修改成功-----'
        self.log.info(text)
        percent1 = random.randint(1, 100)
        percent2 = random.randint(1, 4294967295)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -S {self.Class_Name} -E ' \
                      f'"QualificationTime={percent2},' \
                      f'CPUSkewPercent={percent1}" --penalty;' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        msg2 = msg.split(f'{self.Class_Name}\n')[1]
        self.assertIn(f'PENALTY: QualificationTime={percent2} '
                      f'CPUSkewPercent={percent1}', msg2, '执行失败' + text)

        text = '-----step3:设置CPUSkewPercent为1-100的unint型，且设置' \
               'QualificationTime为1-4294967295的uint型，' \
               '指定异常操作abort  expect:修改成功-----'
        self.log.info(text)
        percent3 = random.randint(1, 100)
        percent4 = random.randint(1, 4294967295)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -S {self.Class_Name} -E ' \
                      f'"QualificationTime={percent4},' \
                      f'CPUSkewPercent={percent3}" --a;' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        msg2 = msg.split(f'{self.Class_Name}\n')[1]
        self.assertIn(f'ABORT: QualificationTime={percent4} '
                      f'CPUSkewPercent={percent3} \n'
                      f'PENALTY: QualificationTime={percent2} '
                      f'CPUSkewPercent={percent1}', msg2, '执行失败' + text)

    def tearDown(self):
        self.log.info('-----step4:清理环境-----')
        text = '-----gs_cgroup --revert恢复cgroup配置 expect:恢复成功-----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};'\
            f'gs_cgroup --revert'
        msg = self.primary_node.sh(execute_cmd).result()
        self.assertEqual('', msg, '执行失败' + text)
        self.log.info(f'-----{os.path.basename(__file__)[:-3]}end-----')
