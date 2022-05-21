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
Case Name   : 指定执行场景测试的结果输出路径(路径无权限)，以binary_upgrade场景为例
Description :
     1.指定执行场景测试的结果输出路径(路径无权限)，以binary_upgrade场景为例
Expect      :
     1.权限拒绝，无法产生结果报告
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Tools_gs_check_Case0366start---')
        self.dbusernode = Node('dbuser')
        self.rootnode = Node('default')
        self.constant = Constant()

    def test_server_tools1(self):
        self.log.info('---步骤1：指定执行场景测试的结果输出路径(路径无权限)，以binary_upgrade场景为例---')
        mkdir_cmd = f'mkdir  {macro.DB_INSTANCE_PATH}/checkresult;'
        self.log.info(mkdir_cmd)
        mkdir_msg = self.rootnode.sh(mkdir_cmd).result()
        self.log.info(mkdir_msg)
        result_path = f'{macro.DB_INSTANCE_PATH}/checkresult'
        check_cmd1 = f'''source {macro.DB_ENV_PATH}; \
            gs_check -e binary_upgrade -o {result_path};
            '''
        self.log.info(check_cmd1)
        check_msg1 = self.dbusernode.sh(check_cmd1).result()
        self.log.info(check_msg1)
        self.assertIn('Permission denied', check_msg1)

    def tearDown(self):
        self.log.info('------清理环境-------')
        clear_cmd1 = f'rm -rf {macro.DB_INSTANCE_PATH}/checkresult;'
        self.log.info(clear_cmd1)
        clear_msg1 = self.rootnode.sh(clear_cmd1).result()
        self.log.info(clear_msg1)
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0366finish--')
