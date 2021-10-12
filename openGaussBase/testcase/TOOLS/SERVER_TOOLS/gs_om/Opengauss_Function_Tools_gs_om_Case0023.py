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
Case Name   : 数据库启动时，指定-D
Description :
    1.查看数据库状态
    2.停止数据库
    3.启动时，指定-D 后面无具体路径是否启动成功
    4.启动时，指定-D 路径有误是否启动成功
    5.启动时，指定-D 路径正确是否启动成功
    6.查看数据库状态
Expect      :
    1.状态正常
    2.关闭数据库
    3.执行失败
    4.执行失败
    5.启动成功
    6.状态正常
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
        self.logger.info('----Opengauss_Function_Tools_gs_om_Case0023start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()
        self.dn1 = macro.DB_INSTANCE_PATH

    def test_server_tools1(self):
        self.logger.info('-----------------查看数据库状态-------------------')
        status_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_om  -t status --detail 
            '''
        self.logger.info(status_cmd1)
        status_msg = self.dbuser_node.sh(status_cmd1).result()
        self.logger.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)
        self.logger.info('------------------停止数据库------------------')
        stop_cmd = self.commonsh.stop_db_cluster()
        self.logger.info(stop_cmd)
        self.assertTrue(stop_cmd)
        self.logger.info('--启动时，指定-D 后面无具体路径是否启动成功--')
        start_cmd1 = f'source {macro.DB_ENV_PATH}; gs_om  -t start -D;'
        self.logger.info(start_cmd1)
        start_msg1 = self.dbuser_node.sh(start_cmd1).result()
        self.logger.info(start_msg1)
        self.assertIn('option -D requires argument', start_msg1)
        self.logger.info('------启动时，指定-D 路径有误是否启动成功-------')
        self.error_msg = 'The input dataDir(/opt/qumin/cluster/dn1) may ' \
                         'be incorrect'
        start_cmd2 = f'''source {macro.DB_ENV_PATH};
            gs_om  -t start -D /opt/qumin/cluster/dn1;
            '''
        self.logger.info(start_cmd2)
        start_msg2 = self.dbuser_node.sh(start_cmd2).result()
        self.logger.info(start_msg2)
        self.assertIn(self.error_msg, start_msg2)
        self.logger.info('---启动时，指定-D 路径正确是否启动成功---')
        start_cmd3 = f'''source {macro.DB_ENV_PATH}; 
            gs_om  -t start -D {self.dn1};
            '''
        self.logger.info(start_cmd3)
        start_msg3 = self.dbuser_node.sh(start_cmd3).result()
        self.logger.info(start_msg3)
        self.assertIn(self.constant.GS_OM_START_SUCCESS_MSG, start_msg3)
        self.logger.info('----------------查询数据库状态-----------------')
        status_cmd2 = self.commonsh.get_db_cluster_status()
        self.logger.info(status_cmd2)
        self.assertTrue("Degraded" in status_cmd2 or "Normal" in status_cmd2)

    def tearDown(self):
        self.logger.info('------------------启动数据库------------------')
        start_cmd = self.commonsh.start_db_cluster()
        self.logger.info(start_cmd)
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0023finish---')
