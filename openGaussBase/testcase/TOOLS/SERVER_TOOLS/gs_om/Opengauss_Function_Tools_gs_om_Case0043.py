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
Case Name   : 数据库关闭时，不指定-D
Description :
    1.查看数据库状态：gs_om -t status --detail
    2.停止数据库时，不指定-D：gs_om -t stop;
    3.启动数据库:gs_om -t start
Expect      :
    1.状态正常
    2.关闭数据库
    3.启动成功
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
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0043start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.logger.info('---------------查看数据库状态-----------------')
        status_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_om -t status --detail ;
            '''
        self.logger.info(status_cmd1)
        status_msg1 = self.dbuser_node.sh(status_cmd1).result()
        self.logger.info(status_msg1)
        self.assertTrue("Degraded" in status_msg1 or "Normal" in status_msg1)
        self.logger.info('----------关闭数据库时，不指定-D-------------')
        certificate_path = os.path.join(macro.DB_INSTANCE_PATH, 'server.*')
        ls_cmd = f"ls -l {certificate_path}"
        self.logger.info(ls_cmd)
        stop_cmd = f'source {macro.DB_ENV_PATH}; gs_om -t stop ;'
        self.logger.info(stop_cmd)
        stop_msg = self.dbuser_node.sh(stop_cmd).result()
        self.logger.info(stop_msg)
        self.assertIn(self.constant.GS_OM_STOP_SUCCESS_MSG, stop_msg)

    def tearDown(self):
        self.logger.info('------------------启动数据库------------------')
        start_cmd = self.commonsh.start_db_cluster()
        self.logger.info(start_cmd)
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0043finish--')