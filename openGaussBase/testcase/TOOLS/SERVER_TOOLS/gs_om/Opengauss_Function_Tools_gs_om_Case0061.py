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
Case Type   : 服务端工具
Case Name   : 查询数据库状态时显示详细信息
Description :
    1.查询数据库状态:gs_om -t status
    2.查询数据库状态时，显示详细信息:gs_om -t status --detail
Expect      :
    1.只提示该服务器正常
    2.显示数据库详细信息,状态正常
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
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0061start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.logger.info('---------------查看数据库状态----------------')
        status_cmd1 = f'''source {macro.DB_ENV_PATH}; gs_om -t status'''
        self.logger.info(status_cmd1)
        status_msg1 = self.dbuser_node.sh(status_cmd1).result()
        self.logger.info(status_msg1)
        self.assertIn(self.constant.GS_OM_STATUS_MSG1, status_msg1)

        self.logger.info('--------查询数据库状态时，显示详细信息----------')
        status_cmd2 = f'source {macro.DB_ENV_PATH}; gs_om -t status --detail;'
        self.logger.info(status_cmd2)
        status_msg2 = self.dbuser_node.sh(status_cmd2).result()
        self.logger.info(status_msg2)
        self.assertIn('Primary Normal', status_msg2)

    def tearDown(self):
        self.logger.info('--------------无需清理环境-------------------')
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0061finish--')
