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
Case Name   : gs_cgroup --recover 回退Class控制组和Workload控制组的增删改操作，且只能回退一次
Description :
    1.omm用户下执行gs_cgroup -c -S {classname} -G {grpname}  创建控制组
    2.omm用户下执行gs_cgroup -d -S {classname}  删除控制组
    3.omm用户下执行gs_cgroup --recover   回退操作
    4.omm用户下执行gs_cgroup --recover   回退操作
    5.gs_cgroup --revert清理环境
Expect      :
    1.创建成功
    2.删除成功
    3.回退成功
    4.回退失败
    5.环境清理成功
History     :
"""
import unittest

from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Cgroup_Case0003开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.Class_Name = 'Gs_Cgroup_Case0003_class'
        self.Grp_Name = 'Gs_Cgroup_Case0003_grp'

    def test_gs_cgroup(self):
        text = '----step1:创建控制组 expect:创建成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --revert;' \
                      f'gs_cgroup -c -S {self.Class_Name} -G {self.Grp_Name};' \
                      f'gs_cgroup -p'
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.Class_Name, msg, '执行失败' + text)
        self.assertIn(self.Grp_Name, msg, '执行失败' + text)

        text = '----step2:删除控制组 expect:删除成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup -d -S {self.Class_Name};' \
                      f'gs_cgroup -p'
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertNotIn(self.Class_Name, msg, '执行失败' + text)
        self.assertNotIn(self.Grp_Name, msg, '执行失败' + text)

        text = '----step3:回退控制组状态 expect:回退成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --recover;' \
                      f'gs_cgroup -p'
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.Class_Name, msg, '执行失败' + text)
        self.assertIn(self.Grp_Name, msg, '执行失败' + text)

        text = '----step4:回退控制组状态 expect:回退失败----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'gs_cgroup --recover;' \
                      f'gs_cgroup -p'
        msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.Class_Name, msg, '执行失败' + text)
        self.assertIn(self.Grp_Name, msg, '执行失败' + text)

    def tearDown(self):
        self.log.info('----step5:清理环境----')
        text = '----gs_cgroup --revert恢复cgroup配置 expect:恢复成功----'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};'\
            f'gs_cgroup --revert'
        msg = self.primary_node.sh(execute_cmd).result()
        self.assertEqual('', msg, '执行失败' + text)
        self.log.info(
            '----Opengauss_Function_Gs_Cgroup_Case0003执行完成----')
