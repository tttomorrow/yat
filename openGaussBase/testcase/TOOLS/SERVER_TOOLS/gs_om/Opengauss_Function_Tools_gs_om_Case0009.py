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
Case Name   : gs_om命令的类型:start、stop、status、query
Description :
    1.查询数据库状态:gs_om -t status
    2.停止数据库:gs_om -t stop
    3.启动数据库：gs_om -t start
    4.查询数据库详细状态信息：gs_om -t query
Expect      :
    1.状态显示成功
    2.关闭成功
    3.启动成功
    4.正确显示数据库状态信息
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0009start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.logger.info('----------------查询数据库状态----------------')
        status_cmd1 = f'source {macro.DB_ENV_PATH}; gs_om -t status;'
        self.logger.info(status_cmd1)
        status_msg1 = self.dbuser_node.sh(status_cmd1).result()
        self.logger.info(status_msg1)
        self.assertTrue("Degraded" in status_msg1 or "Normal" in status_msg1)
        self.logger.info('------------------停止数据库------------------')
        certificate_path = os.path.join(macro.DB_INSTANCE_PATH, 'server.*')
        ls_cmd = f"ls -l {certificate_path}"
        self.logger.info(ls_cmd)
        stop_cmd = self.commonsh.stop_db_cluster()
        self.logger.info(stop_cmd)
        self.assertTrue(stop_cmd)

        self.logger.info('------------------启动数据库------------------')
        start_cmd = self.commonsh.start_db_cluster()
        self.logger.info(start_cmd)
        self.assertTrue(start_cmd)
        self.logger.info('----------查询数据库详细状态信息----------')
        query_cmd = f'source {macro.DB_ENV_PATH};gs_om -t query;'
        self.logger.info(query_cmd)
        query_msg = self.dbuser_node.sh(query_cmd).result()
        self.logger.info(query_msg)
        self.assertTrue("Degraded" in query_msg or "Normal" in query_msg)

    def tearDown(self):
        self.logger.info('------------------启动数据库------------------')
        start_cmd = self.commonsh.start_db_cluster()
        self.logger.info(start_cmd)
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0009finish--')
