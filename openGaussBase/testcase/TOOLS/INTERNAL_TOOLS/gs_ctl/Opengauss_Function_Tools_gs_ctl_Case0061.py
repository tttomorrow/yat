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
Case Name   : 主机执行gs_ctl promote使用-D指定正确数据库实例目录是否合理报错
Description :
    1.执行gs_ctl promote指定-D设置参数为正确的数据库实例目录(主机执行)
Expect      :
    1.执行gs_ctl promote指定-D设置参数为正确的数据库实例目录失败
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('----------------this is setup-------------------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0061开始执行-----')
        self.constant = Constant()
        self.user_node = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('--------------------执行promote---------------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl promote -D {macro.DB_INSTANCE_PATH} ;
            '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn('server is not in standby mode', msg)

    def tearDown(self):
        LOG.info('----------------this is tearDown--------------')
        # 无需清理环境
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0061执行完成----')
