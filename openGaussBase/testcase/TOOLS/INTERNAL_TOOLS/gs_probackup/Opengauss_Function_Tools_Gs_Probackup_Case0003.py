"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Type   : 系统内部使用工具
Case Name   : 使用gs_probackup version查看数据库版本
Description :
    1.使用gs_probackup工具查看数据库版本
Expect      :
    1.使用gs_probackup工具查看数据库版本成功
History     :
"""

import unittest

from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup--------------------')
        LOG.info('---Opengauss_Function_Tools_Gs_Probackup_Case0003开始执行---')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.constant = Constant()

    def test_system_internal_tools(self):
        LOG.info('----执行命令打印编译数据库时使用的LIBS变量的数值---')
        print_cmd = f'''source {macro.DB_ENV_PATH};
            gs_probackup version;'''
        LOG.info(print_cmd)
        print_msg = self.PrimaryNode.sh(print_cmd).result()
        LOG.info(print_msg)
        self.assertIn('openGauss', print_msg)

    def tearDown(self):
        LOG.info('-----------------this is tearDown-------------------')
        # 无需清理环境
        LOG.info('---Opengauss_Function_Tools_Gs_Probackup_Case0003执行完成---')
