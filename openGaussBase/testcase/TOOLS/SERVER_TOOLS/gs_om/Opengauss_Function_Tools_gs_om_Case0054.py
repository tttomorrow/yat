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
Case Name   : 关闭数据库，设置超时时间和日志路径
Description :
    1.查看数据库状态
    2.关闭数据库时指定-l,设置超时时间是否可以关闭成功
    3.启动数据库
    4.查看数据库状态
Expect      :
    1.状态正常
    2.关闭数据库
    3.启动成功
    4.状态正常
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
        self.log = Logger()
        self.log.info('---Opengauss_Function_Tools_gs_om_Case0054start---')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.log.info('-----------------步骤1：查看数据库状态-------------------')
        status_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail;'
        self.log.info(status_cmd1)
        status_msg1 = self.dbuser_node.sh(status_cmd1).result()
        self.log.info(status_msg1)
        self.assertTrue("Degraded" in status_msg1 or "Normal" in status_msg1)
        self.log.info('---步骤2.1：关闭数据库,设置超时时间并将日志放在指定路径下---')
        certificate_path1 = os.path.join(macro.DB_INSTANCE_PATH, 'server.*')
        ls_cmd1 = f'ls -l {certificate_path1};'
        self.log.info(ls_cmd1)
        stop_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_om ' \
            f'-t stop ' \
            f'--time-out=268 ' \
            f'-l {macro.DB_INSTANCE_PATH}/omlog/gs_om.log;'
        self.log.info(stop_cmd1)
        stop_msg1 = self.dbuser_node.sh(stop_cmd1).result()
        self.log.info(stop_msg1)
        self.assertIn(self.constant.GS_OM_STOP_SUCCESS_MSG, stop_msg1)
        self.log.info('------步骤2.2查询是否生成日志文件-------')
        cat_cmd1 = f'cat {macro.DB_INSTANCE_PATH}/omlog/gs_om*;'
        cat_msg1 = self.dbuser_node.sh(cat_cmd1).result()
        self.log.info(cat_msg1)
        self.assertIn('Operation succeeded: Stop', cat_msg1)
        self.log.info('------步骤2.3：清理生成的日志文件-------')
        clear_cmd1 = f'rm -rf {macro.DB_INSTANCE_PATH}/omlog;'
        self.log.info(clear_cmd1)
        clear_msg1 = self.dbuser_node.sh(clear_cmd1).result()
        self.log.info(clear_msg1)
        self.log.info('----------步骤3：启动数据库-----------')
        start_cmd1 = f'source {macro.DB_ENV_PATH};gs_om -t start;'
        self.log.info(start_cmd1)
        start_msg1 = self.dbuser_node.sh(start_cmd1).result()
        self.log.info(start_msg1)
        self.assertIn(self.constant.GS_OM_START_SUCCESS_MSG, start_msg1)
        self.log.info('-----------------步骤4：查看数据库状态-------------------')
        status_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail;'
        self.log.info(status_cmd1)
        status_msg1 = self.dbuser_node.sh(status_cmd1).result()
        self.log.info(status_msg1)
        self.assertTrue("Degraded" in status_msg1 or "Normal" in status_msg1)

    def tearDown(self):
        self.log.info('------------恢复环境-------------')
        start_cmd3 = f'source {macro.DB_ENV_PATH};gs_om -t start;'
        self.log.info(start_cmd3)
        start_msg3 = self.dbuser_node.sh(start_cmd3).result()
        self.log.info(start_msg3)
        self.log.info('--Opengauss_Function_Tools_gs_om_Case0054finish--')
