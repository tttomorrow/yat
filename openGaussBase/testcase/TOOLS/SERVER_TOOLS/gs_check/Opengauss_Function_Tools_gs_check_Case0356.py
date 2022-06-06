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
Case Name   : 使用参数-e 在本地执行health（健康检查巡检场景）
Description :
    1. 使用参数-e 和-L在本地执行health（健康检查巡检场景）
Expect      :
    1.巡检成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0356start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.log.info('---步骤1.在本地执行health（健康检查巡检场景）---')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_check -e health -L '
        self.log.info(check_cmd)
        check_msg = self.dbuser_node.sh(check_cmd).result()
        self.log.info(check_msg)
        check_result_flag = False
        for single_msg in self.constant.GS_CHECK_SUCCESS_MSG1:
            if single_msg in check_msg:
                check_result_flag = True
        self.assertTrue(check_result_flag)

    def tearDown(self):
        self.log.info("--------------无需清理环境---------------")
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0356finish--')
