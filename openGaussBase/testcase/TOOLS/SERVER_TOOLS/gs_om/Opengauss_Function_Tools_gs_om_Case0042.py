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
Case Name   : 数据库关闭时，指定日志存放路径
Description :
    1.查看数据库状态：gs_om -t status --detail
    2.关闭数据库时，指定日志文件存放路径不正确
    3.查看数据库状态：gs_om -t status --detail
    4.关闭数据库时，指定日志文件存放路径
    5.在指定路径下
    6.查看数据库状态：gs_om -t status --detail
    7.启动数据库：gs_om -t start
    8.查看数据库状态：gs_om -t status --detail
    9.删除日志文件
Expect      :
    1.状态正常
    2.执行失败
    3.状态正常
    4.关闭数据库
    5.查看日志成功
    6.状态不可用
    7.启动成功
    8.状态成功
    9.删除成功
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
        self.log.info('---Opengauss_Function_Tools_gs_om_Case0042start---')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.log.info('-----------------查看数据库状态-------------------')
        status_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail ;'
        self.log.info(status_cmd)
        status_msg = self.dbuser_node.sh(status_cmd).result()
        self.log.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)

        self.log.info('----------关闭数据库时，指定日志文件存放路径不正确----------')
        certificate_path = os.path.join(macro.DB_INSTANCE_PATH, 'server.*')
        ls_cmd = f'ls -l {certificate_path}'
        self.log.info(ls_cmd)
        stop_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_om -t stop -l {macro.DB_INSTANCE_PATH}/omlog.txt;'
        self.log.info(stop_cmd)
        stop_msg = self.dbuser_node.sh(stop_cmd).result()
        self.log.info(stop_msg)
        self.assertIn('omlog.txt] should be \'.log\'', stop_msg)

        self.log.info('-----------------查看数据库状态-------------------')
        status_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail ;'
        self.log.info(status_cmd)
        status_msg = self.dbuser_node.sh(status_cmd).result()
        self.log.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)

        self.log.info('-----------------启动数据库-------------------')
        start_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_om -t start;'
        self.log.info(start_cmd)
        start_msg = self.dbuser_node.sh(start_cmd).result()
        self.log.info(start_msg)
        self.assertIn(self.constant.GS_OM_START_SUCCESS_MSG, start_msg)

        self.log.info('-----------------查看数据库状态-------------------')
        status_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail ;'
        self.log.info(status_cmd)
        status_msg = self.dbuser_node.sh(status_cmd).result()
        self.log.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)

        self.log.info('----------关闭数据库时，指定日志文件存放路径----------')
        certificate_path = os.path.join(macro.DB_INSTANCE_PATH, 'server.*')
        ls_cmd = f'ls -l {certificate_path}'
        self.log.info(ls_cmd)
        stop_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_om -t stop -l {macro.DB_INSTANCE_PATH}/omlog.log;'
        self.log.info(stop_cmd)
        stop_msg = self.dbuser_node.sh(stop_cmd).result()
        self.log.info(stop_msg)
        self.assertIn(self.constant.GS_OM_STOP_SUCCESS_MSG, stop_msg)

        self.log.info('---查看日志---')
        cat_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'cat {macro.DB_INSTANCE_PATH}/omlog*'
        self.log.info(cat_cmd)
        cat_msg = self.dbuser_node.sh(cat_cmd).result()
        self.log.info(cat_msg)
        self.assertIn('succeeded: Stop', cat_msg)

        self.log.info('-----------------查看数据库状态-------------------')
        status_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail ;'
        self.log.info(status_cmd)
        status_msg = self.dbuser_node.sh(status_cmd).result()
        self.log.info(status_msg)
        self.assertTrue('stopped', status_msg)

        self.log.info('-----------------启动数据库-------------------')
        start_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_om -t start;'
        self.log.info(start_cmd)
        start_msg = self.dbuser_node.sh(start_cmd).result()
        self.log.info(start_msg)
        self.assertIn(self.constant.GS_OM_START_SUCCESS_MSG, start_msg)

        self.log.info('-----------------查看数据库状态-------------------')
        status_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail ;'
        self.log.info(status_cmd)
        status_msg = self.dbuser_node.sh(status_cmd).result()
        self.log.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)

    def tearDown(self):
        self.log.info('------------清理环境，启动数据库-------------')
        rm_cmd = f'source {macro.DB_ENV_PATH};' \
            f'rm -rf {macro.DB_INSTANCE_PATH}/omlog*'
        self.log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        self.log.info(rm_msg)
        start_cmd = self.commonsh.start_db_cluster()
        self.log.info(start_cmd)
        self.log.info('--Opengauss_Function_Tools_gs_om_Case0042finish--')
