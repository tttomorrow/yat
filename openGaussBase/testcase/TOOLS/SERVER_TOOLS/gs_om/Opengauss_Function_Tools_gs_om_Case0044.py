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
Case Name   : 数据库关闭时，指定-D
Description :
    1.查看数据库状态：gs_om -t status --detail
    2.停止数据库时，指定-D 后面无具体路径是否关闭成功
    3.停止数据库时，指定-D 路径有误是否关闭成功
    4.停止数据库时，指定-D 路径正确是否关闭成功
    5.启动数据库:gs_om -t start
Expect      :
    1.状态正常
    2.执行失败
    3.执行失败
    4.关闭数据库
    5.启动成功
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
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0044start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()
        self.dn1 = macro.DB_INSTANCE_PATH

    def test_server_tools1(self):
        self.logger.info('--------------查看数据库状态-----------------')
        status_cmd1 = f'''source {macro.DB_ENV_PATH}; 
            gs_om  -t status --detail;
            '''
        self.logger.info(status_cmd1)
        status_msg1 = self.dbuser_node.sh(status_cmd1).result()
        self.logger.info(status_msg1)
        self.assertTrue("Degraded" in status_msg1 or "Normal" in status_msg1)
        self.logger.info('----关闭时，指定-D 后面无具体路径是否关闭成功----')
        stop_cmd1 = f'''source {macro.DB_ENV_PATH};gs_om  -t stop -D ;'''
        self.logger.info(stop_cmd1)
        stop_msg1 = self.dbuser_node.sh(stop_cmd1).result()
        self.logger.info(stop_msg1)
        self.assertIn('option -D requires argument', stop_msg1)
        self.logger.info('-----关闭时，指定-D 路径有误是否关闭成功------')
        self.error_msg = "The input dataDir(/opt/qumin/cluster/dn1) may " \
                         "be incorrect"
        stop_cmd2 = f'''source {macro.DB_ENV_PATH};
            gs_om  -t stop -D /opt/qumin/cluster/dn1 ;
            '''
        self.logger.info(stop_cmd2)
        stop_msg2 = self.dbuser_node.sh(stop_cmd2).result()
        self.logger.info(stop_msg2)
        self.assertIn(self.error_msg, stop_msg2)
        self.logger.info('-----关闭时，指定-D 路径正确是否关闭成功------')
        certificate_path = os.path.join(macro.DB_INSTANCE_PATH, 'server.*')
        ls_cmd = f"ls -l {certificate_path}"
        self.logger.info(ls_cmd)
        stop_cmd3 = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_om  -t stop -D {self.dn1}; '
        self.logger.info(stop_cmd3)
        stop_msg3 = self.dbuser_node.sh(stop_cmd3).result()
        self.logger.info(stop_msg3)
        self.assertIn(self.constant.GS_OM_STOP_SUCCESS_MSG, stop_msg3)

    def tearDown(self):
        self.logger.info('------------------启动数据库------------------')
        start_cmd = self.commonsh.start_db_cluster()
        self.logger.info(start_cmd)
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0044finish--')
