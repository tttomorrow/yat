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
Case Name   : Class组下自定义class组更改{classname}组cpu占用资源比例相加超过100%
Description :
    1.omm用户下执行gs_cgroup -c -S {classname1}
    创建class1控制组
    2.omm用户下执行gs_cgroup -c -S {classname2}
    创建class2控制组
    3.omm用户下执行gs_cgroup -u --fixed -S {classname1} -s 51
    4.omm用户下执行gs_cgroup -u --fixed -S {classname2} -s 51
    5.gs_cgroup --revert清理环境
Expect      :
    1.创建成功
    2.创建成功
    3.修改成功
    4.修改失败
    5.环境清理成功
History     :
"""
import unittest
import os
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)[:-3]}开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.Class_Name1 = 'Cgroup_Case0072_class1'
        self.Class_Name2 = 'Cgroup_Case0072_class2'

    def test_gs_cgroup(self):
        text = '----step1:创建class1控制组 expect:创建成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
                      f'gs_cgroup -c -S {self.Class_Name1};' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.Class_Name1, msg, '执行失败' + text)
        text = '----step2:创建class2控制组 expect:创建成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -c -S {self.Class_Name2};' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.Class_Name2, msg, '执行失败' + text)
        text = '----step3:更改class1组cpu资源利用51 expect:修改成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -u --fixed -S {self.Class_Name1} -s 51;' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        class1_msg = msg.split(f'{self.Class_Name1}')[1].split(f'Cores')[0]
        self.assertIn(f'Quota(%): 51', class1_msg, '执行失败' + text)

        text = '----step4:更改class2组cpu资源利用51 expect:修改失败----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -u --fixed -S {self.Class_Name2} -s 51;' \
                      f'gs_cgroup -p'
        self.log.info(execute_cmd)
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        error_msg = f'ERROR: the total percentage of cpu cores are larger th' \
                    f'an 100, you cannot set 51% for group "{self.Class_Name2}"'
        self.assertIn(error_msg, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----step5:清理环境----')
        text = '----gs_cgroup --revert恢复cgroup配置 expect:恢复成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};'\
            f'gs_cgroup --revert'
        msg = self.primary_node.sh(execute_cmd).result()
        self.assertEqual('', msg, '执行失败' + text)
        self.log.info(f'----{os.path.basename(__file__)[:-3]}执行完成----')
