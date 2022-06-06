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
Case Name   : 升级巡检场景检查，跳过root权限检查项，在指定路径下生成log文件和检查结果文件，并设置超时时间为1800
Description :
     1.升级巡检场景检查，跳过root权限检查项，在指定路径下生成log文件和检查结果文件，并设置超时时间为1800
     2.检查指定路径下是否生成log文件和检查结果文件
     3.删除生成的文件
Expect      :
     1.场景检查完成并在指定路径下产生日志文件
     2.指定路径下生成log文件
     3.删除生成的文件
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Tools_gs_check_Case0386start---')
        self.dbusernode = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        self.log.info('---步骤1：升级巡检场景检查，跳过root权限检查项，并生成log文件，并设置超时时间为1800---')
        mkdir_cmd = f'mkdir {macro.DB_INSTANCE_PATH}/checkresult;'
        self.log.info(mkdir_cmd)
        mkdir_msg = self.dbusernode.sh(mkdir_cmd).result()
        self.log.info(mkdir_msg)
        check_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_check ' \
            f'-e upgrade ' \
            f'--skip-root-items ' \
            f'-l {macro.DB_INSTANCE_PATH}/checklog/gs_check.log ' \
            f'-o {macro.DB_INSTANCE_PATH}/checkresult ' \
            f'--time-out 1800;'
        self.log.info(check_cmd1)
        msg1 = self.dbusernode.sh(check_cmd1).result()
        self.log.info(msg1)
        flag = (self.constant.GS_CHECK_SUCCESS_MSG2[0] in msg1 or
                self.constant.GS_CHECK_SUCCESS_MSG2[1] in msg1) and \
                self.constant.GS_CHECK_SUCCESS_MSG2[2] in msg1
        self.assertTrue(flag)
        self.log.info('---------------步骤2.1：判断是否产生日志文件---------------')
        cat_cmd1 = f'cat {macro.DB_INSTANCE_PATH}/checklog/gs_check* ;'
        cat_msg1 = self.dbusernode.sh(cat_cmd1).result()
        self.log.info(cat_msg1)
        self.assertIn('Analysis the check result successfully', cat_msg1)
        self.log.info('---------------步骤2.2：判断是否产生结果报告---------------')
        cat_cmd = f'cd  {macro.DB_INSTANCE_PATH}/checkresult;' \
            f'tar -xvf CheckReport_upgrade*.tar.gz; ' \
            f'cat CheckResult*;'
        cat_msg = self.dbusernode.sh(cat_cmd).result()
        self.log.info(cat_msg)
        self.assertIn('All check items run completed', cat_msg)

    def tearDown(self):
        self.log.info('------步骤3：清理生成的日志文件和结果报告-------')
        clear_cmd1 = f'rm -rf {macro.DB_INSTANCE_PATH}/checklog;' \
            f'rm -rf {macro.DB_INSTANCE_PATH}/checkresult;'
        self.log.info(clear_cmd1)
        clear_msg1 = self.dbusernode.sh(clear_cmd1).result()
        self.log.info(clear_msg1)
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0386finish--')
